# Generated by Django 2.1.5 on 2024-08-22 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0022_plaidaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(default='OTHER', max_length=20),
        ),
    ]
