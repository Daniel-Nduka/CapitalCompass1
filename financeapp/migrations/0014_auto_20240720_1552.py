# Generated by Django 2.1.5 on 2024-07-20 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0013_userprofile_last_accessed_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='assigned_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
