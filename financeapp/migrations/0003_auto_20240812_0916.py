# Generated by Django 2.1.5 on 2024-08-12 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0002_zerobasedcategory_month_only'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='zerobasedcategory',
            unique_together={('budget', 'name', 'month_only')},
        ),
    ]
