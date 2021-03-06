# Generated by Django 2.0.3 on 2018-03-16 15:23

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vigil', '0029_auto_20180316_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreProcessorAlertAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('last_triggered', models.DateTimeField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vigil.PreProcessorActionTask')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
