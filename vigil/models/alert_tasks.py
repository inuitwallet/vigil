from django.contrib.postgres.fields import JSONField
from django.db import models


class ActionTask(models.Model):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class LogicActionTask(ActionTask):
    expected_data = JSONField(
        default=dict,
        blank=True,
    )
    business_logic_data = JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return self.name


class PreProcessorActionTask(ActionTask):
    """
    Accept POST Data as defined in self.expected data
    Process that data into a meaningful 'Title', 'Message' and 'Priority' as
    required by a NotificationActionTask.
    Each Alert Channel is expected to have one PreProcessorActionTask to define
    where the alert data is coming from and in what format
    """
    expected_data = JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return self.name


class NotificationActionTask(ActionTask):
    default_data = JSONField(
        default=dict,
        blank=True,
        help_text='The data required for the notification task to function. '
                  'Normally API details or similar'
    )

    def __str__(self):
        return self.name
