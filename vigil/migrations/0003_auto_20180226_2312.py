# Generated by Django 2.0.2 on 2018-02-26 23:12

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigil', '0002_auto_20180226_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertaction',
            name='action_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alertaction',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='alertaction',
            name='last_triggered',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alertchannel',
            name='alert_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alertchannel',
            name='alert_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
