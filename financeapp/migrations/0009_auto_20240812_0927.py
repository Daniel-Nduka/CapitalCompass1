# Generated by Django 2.1.5 on 2024-08-12 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0008_auto_20240812_0925'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fiftythirtytwentycategory',
            unique_together={('budget', 'name')},
        ),
    ]
