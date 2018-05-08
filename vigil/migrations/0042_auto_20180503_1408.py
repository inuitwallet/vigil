# Generated by Django 2.0.3 on 2018-05-03 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vigil', '0041_auto_20180503_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logicalertaction',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action_tasks', related_query_name='action_task', to='vigil.LogicActionTask'),
        ),
        migrations.AlterField(
            model_name='notificationalertaction',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action_tasks', related_query_name='action_task', to='vigil.NotificationActionTask'),
        ),
        migrations.AlterField(
            model_name='preprocessoralertaction',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action_tasks', related_query_name='action_task', to='vigil.PreProcessorActionTask'),
        ),
    ]
