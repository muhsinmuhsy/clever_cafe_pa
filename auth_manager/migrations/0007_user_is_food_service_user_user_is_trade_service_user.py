# Generated by Django 5.0.7 on 2024-08-07 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_manager', '0006_alter_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_food_service_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_trade_service_user',
            field=models.BooleanField(default=False),
        ),
    ]
