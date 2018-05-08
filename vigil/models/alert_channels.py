from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from vigil.globals import priorities, bootstrap_priorities


class AlertChannel(models.Model):
    name = models.CharField(
        max_length=255,
        help_text='The name for this Alert Channel'
    )
    alert_id = models.UUIDField(
        default=uuid4,
        editable=False
    )
    preprocessor_action = models.ForeignKey(
        'PreProcessorAlertAction',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='This action will be used to pre-process incoming alert data to '
                  'format a title, message and priority for the alert'
    )
    logic_actions = models.ManyToManyField(
        'LogicAlertAction',
        related_name='logic_actions',
        blank=True,
        help_text='Logic Actions process the incoming alert data \n'
                  '(highlighted entries are added. Ctrl+select to choose multiple)'
    )
    notification_actions = models.ManyToManyField(
        'NotificationAlertAction',
        related_name='notification_actions',
        blank=True,
        help_text='Notification Actions are attached to this Alert Channel\n'
                  '(highlighted entries are added. Ctrl+select to choose multiple)'
    )
    repeat_time = models.DurationField(
        default=timedelta(minutes=15),
        help_text='Notification Alert Actions will only be triggered this frequently, '
                  'even if the alert details change'
    )
    time_to_upgrade = models.DurationField(
        default=timedelta(hours=1),
        help_text='After this period, '
                  'the Alert Channel Priority will be upgraded to URGENT'
    )
    auto_acknowledge = models.DurationField(
        default=timedelta(hours=3),
        help_text='If set, alert channels will auto acknowledge if they are not '
                  'updated after this amount of time'
    )
    expected_data = JSONField(
        default=dict,
        blank=True,
        help_text='When activated through the API, this Alert Channel expects these attributes in the POST data'
    )
    base_priority = models.CharField(
        max_length=255,
        choices=priorities,
        default=priorities[0][0]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @property
    def active_alerts(self):
        return self.alert_set.filter(active=True)


@receiver(post_save, sender=AlertChannel)
def post_save(sender, instance, **kwargs):
    keys = []

    if instance.preprocessor_action:
        for key in instance.preprocessor_action.expected_data.keys():
            keys.append(key)

    for logic_action in instance.logic_actions.all():
        for key in logic_action.expected_data.keys():
            keys.append(key)

    expected_data = {}

    for key in set(keys):
        expected_data[key] = ''

    instance.expected_data = expected_data
    instance.save()


class Alert(models.Model):
    alert_channel = models.ForeignKey(
        AlertChannel,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    message = models.TextField(
        blank=True,
        null=True,
    )
    priority = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=priorities,
    )
    active = models.BooleanField(
        default=False,
    )
    alert_created = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )
    last_notification = models.DateTimeField(
        blank=True,
        null=True
    )
    last_priority_change = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return '{} - {}'.format(self.alert_created, self.title)

    class Meta:
        ordering = ['-last_updated']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._previous_priority = self.priority

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.priority != self._previous_priority:
            self.last_priority_change = now()

        super().save(force_insert, force_update, *args, **kwargs)
        self._previous_priority = self.priority

    @property
    def bootstrap_priority(self):
        index = 0

        for priority in priorities:
            if priority[0] == self.priority:
                break
            index += 1

        return bootstrap_priorities[index]
