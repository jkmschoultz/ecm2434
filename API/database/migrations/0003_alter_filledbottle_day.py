# Generated by Django 4.1.7 on 2023-03-10 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_filledbottle_buildingfloor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filledbottle',
            name='day',
            field=models.DateTimeField(),
        ),
    ]
