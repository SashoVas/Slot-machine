# Generated by Django 5.0.1 on 2024-02-09 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0008_alter_roll_cost_alter_roll_winings_multyplier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roll',
            name='cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='roll',
            name='winings_multyplier',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]