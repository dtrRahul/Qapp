# Generated by Django 3.0.6 on 2020-11-24 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0026_auto_20201124_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customers',
            old_name='barber_name',
            new_name='barber',
        ),
    ]