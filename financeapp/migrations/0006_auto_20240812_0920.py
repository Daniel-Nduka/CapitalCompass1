# Generated by Django 2.1.5 on 2024-08-12 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0005_expense_month_only'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='expense',
            unique_together={('fifty_30_twenty_category', 'description', 'month_only'), ('category', 'description', 'month_only')},
        ),
    ]
