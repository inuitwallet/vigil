# Generated by Django 2.0.3 on 2018-03-13 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vigil', '0019_historicalalert'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalalert',
            name='updated',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
