# Generated by Django 5.0.7 on 2024-08-12 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade_service', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ecosystemcriteria',
            old_name='cafe_entrepreneurship_features',
            new_name='ce_features',
        ),
        migrations.RenameField(
            model_name='ecosystemcriteria',
            old_name='cafe_entrepreneurship_menu_highlights',
            new_name='ce_menu_highlights',
        ),
        migrations.RenameField(
            model_name='ecosystemcriteria',
            old_name='cafe_entrepreneurship_operational_status',
            new_name='ce_operational_status',
        ),
        migrations.RenameField(
            model_name='ecosystemcriteria',
            old_name='cafe_entrepreneurship_state',
            new_name='ce_state',
        ),
    ]
