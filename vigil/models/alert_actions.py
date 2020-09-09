from copy import copy

from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import JSONField
from django.db import models

from .task_results import VigilTaskResult


def equalize_json(dict_1, dict_2):
    # check that all necessary keys exist
    for key in dict_1.keys():
        if key not in dict_2.keys():
            dict_2[key] = ''

    # check additional keys don't exist
    dict_2_copy = copy(dict_2)

    for key in dict_2.keys():
        if key not in dict_1.keys():
            del (dict_2_copy[key])

    return dict_2_copy


class AlertAction(models.Model):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    last_triggered = models.DateTimeField(
        blank=True,
        null=True
    )
    task_results = GenericRelation(
        VigilTaskResult,
        related_query_name='task_results',
        content_type_field='alert_task_type',
        object_id_field='alert_task_id',
    )

    class Meta:
        abstract = True


class PreProcessorAlertAction(AlertAction):
    task = models.ForeignKey(
        'PreProcessorActionTask',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='action_tasks',
        related_query_name='action_task'
    )
    expected_data = JSONField(
        default=dict,
        blank=True,
        help_text='The data that is expected from the 3rd party system. '
                  'This forms the basis of a data contract with the 3rd party'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.task:
            self.expected_data = equalize_json(
                self.task.expected_data,
                self.expected_data
            )

        super().save(*args, **kwargs)


class LogicAlertAction(AlertAction):
    task = models.ForeignKey(
        'LogicActionTask',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='action_tasks',
        related_query_name='action_task'
    )
    expected_data = JSONField(
        default=dict,
        blank=True,
        help_text='The data that is expected from the 3rd party system. '
                  'This forms the basis of a data contract with the 3rd party'
    )
    business_logic_data = JSONField(
        default=dict,
        blank=True,
        help_text='The data required from AlertAction to '
                  'allow the business logic to function.'
    )
    notification_actions = models.ManyToManyField(
        'NotificationAlertAction',
        blank=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.task:
            self.expected_data = equalize_json(
                self.task.expected_data,
                self.expected_data
            )
            self.business_logic_data = equalize_json(
                self.task.business_logic_data,
                self.business_logic_data
            )

        super(AlertAction, self).save(*args, **kwargs)


class NotificationAlertAction(AlertAction):
    task = models.ForeignKey(
        'NotificationActionTask',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='action_tasks',
        related_query_name='action_task'
    )
    data = JSONField(
        default=dict,
        blank=True
    )
    last_success = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.task:
            self.data = equalize_json(
                self.task.default_data,
                self.data
            )

        super().save(*args, **kwargs)
