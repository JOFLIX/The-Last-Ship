# Generated by Django 3.1 on 2021-05-21 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incomestatement', '0002_expenses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenses',
            old_name='epenses_amount',
            new_name='expenses_amount',
        ),
        migrations.RenameField(
            model_name='expenses',
            old_name='epenses_name',
            new_name='expenses_name',
        ),
    ]
