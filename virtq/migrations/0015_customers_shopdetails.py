# Generated by Django 3.0.6 on 2020-11-15 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0014_customers_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='shopdetails',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
