# Generated by Django 2.1.5 on 2024-07-15 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0007_budget_currency_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='month',
            field=models.DateField(auto_now_add=True),
        ),
    ]
