# Generated by Django 2.1.5 on 2024-07-24 09:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeapp', '0024_auto_20240724_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiftyThirtyTwentyBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(default=datetime.date.today)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fifty_thirty_twenty_budgets', to='financeapp.Budget')),
            ],
        ),
        migrations.CreateModel(
            name='FiftyThirtyTwentyCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('month', models.DateField(default=datetime.date.today)),
                ('is_recurring', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('Needs', 'Needs'), ('Wants', 'Wants'), ('Savings', 'Savings')], max_length=20)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='financeapp.FiftyThirtyTwentyBudget')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='expense',
            name='fifty_30_twenty_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='financeapp.FiftyThirtyTwentyCategory'),
        ),
    ]
