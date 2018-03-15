from copy import copy
from datetime import timedelta
from uuid import uuid4

from django.contrib.postgres.fields import JSONField
from django.db import models

from django_celery_results.models import TaskResult
from vigil.globals import action_types, priorities


class VigilTaskResult(TaskResult):
    alert_channel = models.ForeignKey(
        'AlertChannel',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    alert_action = models.ForeignKey(
        'AlertAction',
        on_delete=models.CASCADE
    )

    @property
    def clean_result(self):
        return self.result.replace('"', '')

    class Meta:
        ordering = ['-date_done']


class ActionTask(models.Model):
    name = models.CharField(
        max_length=255
    )
    default_data = JSONField(
        default=dict,
        blank=True
    )
    action_type = models.CharField(
        max_length=20,
        choices=action_types
    )

    def __str__(self):
        return self.name


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
    data = JSONField(
        default=dict,
        blank=True
    )
    task = models.ForeignKey(
        ActionTask,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.task:
            # check that all necessary keys exist
            for key in self.task.default_data.keys():
                if key not in self.data.keys():
                    self.data = copy(self.task.default_data)

            # check additional keys don't exist
            data_copy = copy(self.data)
            for key in self.data.keys():
                if key not in self.task.default_data.keys():
                    del(data_copy[key])

            self.data = data_copy

        super(AlertAction, self).save(*args, **kwargs)


class AlertChannel(models.Model):
    name = models.CharField(
        max_length=255,
        help_text='The name for this Alert Channel'
    )
    alert_id = models.UUIDField(
        default=uuid4,
        editable=False
    )
    active = models.BooleanField(
        default=False,
        editable=False
    )
    set_active = models.DateTimeField(
        blank=True,
        null=True,
        editable=False
    )
    title = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        editable=False
    )
    message = models.TextField(
        blank=True,
        null=True,
        editable=False
    )
    priority = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=priorities,
        editable=False
    )
    simple_actions = models.ManyToManyField(
        AlertAction,
        blank=True,
        help_text='Which Alert Actions are attached to this Alert Channel\n'
                  '(highlighted entries are added. Ctrl+select to choose multiple)'
    )
    alert_actions = models.ManyToManyField(
        AlertAction,
        related_name='alert_actions',
        through='ChannelAction',
        blank=True,
        help_text='Which Alert Actions are attached to this Alert Channel\n'
                  '(highlighted entries are added. Ctrl+select to choose multiple)'
    )
    repeat_time = models.DurationField(
        default=timedelta(minutes=15),
        help_text='Alert Actions will only be triggered this frequently, '
                  'even if the alert details change'
    )
    time_to_urgent = models.DurationField(
        default=timedelta(hours=1),
        help_text='After this period, '
                  'the Alert Channel Priority will be upgraded to URGENT'
    )

    def __str__(self):
        return self.name

    @property
    def actions(self):
        return self.alert_actions.order_by('action')

    @property
    def notification_actions(self):
        return self.alert_actions.filter(
            task__action_type='Notification'
        ).order_by(
            'action'
        )

    @property
    def logic_actions(self):
        return self.alert_actions.filter(
            task__action_type='Logic'
        ).order_by(
            'action'
        )


class ChannelAction(models.Model):
    alert_channel = models.ForeignKey(
        AlertChannel,
        related_name='channel',
        on_delete=models.CASCADE
    )
    alert_action = models.ForeignKey(
        AlertAction,
        related_name='action',
        on_delete=models.CASCADE
    )
    priority = models.IntegerField(
        default=0
    )

    def __str__(self):
        return '{} - {} : {}'.format(self.priority, self.alert_channel, self.alert_action)

    class Meta:
        ordering = ['alert_channel', 'priority']


class HistoricalAlert(models.Model):
    alert_channel = models.ForeignKey(
        AlertChannel,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        editable=False
    )
    message = models.TextField(
        blank=True,
        null=True,
        editable=False
    )
    priority = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=priorities,
        editable=False
    )
    alert_created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated = models.BooleanField(
        default=False,
        editable=False
    )

    def __str__(self):
        return '{} - {}'.format(self.alert_created, self.title)

    class Meta:
        ordering = ['-alert_created']

# import the signals file
from vigil import signals
