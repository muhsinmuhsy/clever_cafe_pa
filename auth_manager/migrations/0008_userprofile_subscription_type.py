# Generated by Django 5.0.7 on 2024-08-08 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_manager', '0007_user_is_food_service_user_user_is_trade_service_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='subscription_type',
            field=models.CharField(blank=True, choices=[('lite', 'Lite'), ('pro', 'Pro')], max_length=4, null=True),
        ),
    ]
