# Generated by Django 2.2.1 on 2019-05-10 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cropsold',
            name='crop_weight',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cropsold',
            name='sold',
            field=models.FloatField(),
        ),
    ]
