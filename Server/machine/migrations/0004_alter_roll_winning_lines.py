# Generated by Django 5.0.1 on 2024-01-21 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0003_rename_winings_roll_winings_multyplier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roll',
            name='winning_lines',
            field=models.JSONField(default={}),
        ),
    ]
