# Generated by Django 2.0.3 on 2018-05-04 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vigil', '0048_remove_alertchannel_auto_acknowledge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alertchannel',
            old_name='acknowledge',
            new_name='auto_acknowledge',
        ),
    ]
