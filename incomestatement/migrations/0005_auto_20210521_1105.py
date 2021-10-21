# Generated by Django 3.1 on 2021-05-21 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomestatement', '0004_assets_liabilities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='asset_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='expenses_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='liabilities',
            name='Liabilities_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='revenue',
            name='revenue_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
