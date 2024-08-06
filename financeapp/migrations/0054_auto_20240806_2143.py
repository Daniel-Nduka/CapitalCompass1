# Generated by Django 2.1.5 on 2024-08-06 21:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeapp', '0053_transaction_created_by_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='budget_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='budget',
            unique_together={('user', 'budget_name')},
        ),
    ]
