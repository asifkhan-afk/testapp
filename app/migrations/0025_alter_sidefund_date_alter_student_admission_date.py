# Generated by Django 4.1.1 on 2022-11-12 11:24

import app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_sidefund_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidefund',
            name='date',
            field=models.PositiveIntegerField(blank=True, default=12, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='admission_date',
            field=models.PositiveIntegerField(default=12, validators=[app.validators.validate_date]),
        ),
    ]
