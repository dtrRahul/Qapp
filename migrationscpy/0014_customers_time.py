# Generated by Django 3.0.6 on 2020-11-15 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0013_auto_20200720_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
