# Generated by Django 3.0.6 on 2020-11-22 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0016_barbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='barbers',
            name='shopname',
            field=models.CharField(default=None, max_length=25),
        ),
    ]
