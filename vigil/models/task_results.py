from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_celery_results.models import TaskResult


class VigilTaskResult(TaskResult):
    alert_channel = models.ForeignKey(
        'AlertChannel',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    alert_task_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    alert_task_id = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    alert_task_object = GenericForeignKey(
        'alert_task_type',
        'alert_task_id'
    )

    @property
    def clean_result(self):
        if self.result is not None:
            return self.result.replace('"', '')
        return ''

    class Meta:
        ordering = ['-date_done']
