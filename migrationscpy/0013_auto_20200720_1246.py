# Generated by Django 3.0.6 on 2020-07-20 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0012_auto_20200720_1242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customers',
            old_name='mobile_number',
            new_name='mobile',
        ),
    ]