# Generated by Django 3.2 on 2021-06-21 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210621_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollmentfee',
            name='reg_no',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
