from copy import copy
from datetime import timedelta
from uuid import uuid4

from django.contrib.postgres.fields import JSONField
from django.db import models

from vigil.globals import priorities


class ActionTask(models.Model):
    name = models.CharField(
        max_length=255
    )

    default_data = JSONField(
        default=dict,
        blank=True
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
    actions = models.ManyToManyField(
        AlertAction,
        blank=True,
        help_text='What actions to attach to this Alert Channel'
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
