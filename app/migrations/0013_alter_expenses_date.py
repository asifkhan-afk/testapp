# Generated by Django 3.2.9 on 2022-09-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20220917_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.PositiveIntegerField(blank=True, default=17, null=True),
        ),
    ]
