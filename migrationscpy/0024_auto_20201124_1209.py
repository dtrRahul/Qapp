# Generated by Django 3.0.6 on 2020-11-24 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0023_auto_20201123_2000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customers',
            old_name='barber',
            new_name='hairdresser',
        ),
    ]
