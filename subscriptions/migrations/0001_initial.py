# Generated by Django 5.1.5 on 2025-03-02 03:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier', models.CharField(choices=[('essential', 'Essential'), ('general', 'General'), ('enterprise', 'Enterprise')], max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('features', models.JSONField(default=dict)),
                ('base_monthly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('base_annual_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_contract_months', models.PositiveIntegerField(default=12)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_term', models.CharField(choices=[('yearly', 'Yearly'), ('two_year', 'Two Years'), ('three_year', 'Three Years')], max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('billing_day', models.PositiveSmallIntegerField(help_text='Day of the month billing is processed')),
                ('next_billing_date', models.DateField()),
                ('actual_monthly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('auto_renew', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='subscriptions.subscriptionplan')),
            ],
        ),
    ]
