# Generated by Django 3.0.6 on 2020-11-21 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qapp', '0015_customers_shopdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barbers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('status', models.CharField(default=None, max_length=40)),
            ],
        ),
    ]
