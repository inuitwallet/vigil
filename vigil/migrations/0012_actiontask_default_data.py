# Generated by Django 2.0.2 on 2018-02-27 15:45

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vigil', '0011_auto_20180227_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='actiontask',
            name='default_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]