# Generated by Django 3.1.1 on 2020-10-08 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='active',
        ),
        migrations.AddField(
            model_name='auction',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='Closed'),
        ),
    ]
