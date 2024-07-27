# Generated by Django 2.1.5 on 2024-07-27 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0033_fiftythirtytwentycategory_is_recurring'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiftythirtytwentycategory',
            name='is_user_modified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('CHECKING', 'checking'), ('SAVINGS', 'savings'), ('CASH', 'cash')], max_length=20),
        ),
    ]
