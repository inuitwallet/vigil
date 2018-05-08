# Generated by Django 2.0.3 on 2018-05-04 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigil', '0050_auto_20180504_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alert',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='priority',
            field=models.CharField(blank=True, choices=[('Low', 'LOW'), ('Medium', 'MEDIUM'), ('High', 'HIGH'), ('Urgent', 'URGENT'), ('Emergency', 'EMERGENCY')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
