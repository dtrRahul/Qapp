# Generated by Django 3.0.6 on 2020-06-15 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0003_auto_20200615_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='time',
            field=models.TimeField(),
        ),
    ]
