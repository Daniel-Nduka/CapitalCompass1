# Generated by Django 2.1.5 on 2024-08-21 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0018_plaidaccount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plaidaccount',
            name='account',
        ),
    ]
