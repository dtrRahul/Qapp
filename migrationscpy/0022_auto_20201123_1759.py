# Generated by Django 3.0.6 on 2020-11-23 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0021_auto_20201123_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='barber',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]