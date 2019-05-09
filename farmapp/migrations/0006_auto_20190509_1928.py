# Generated by Django 2.2.1 on 2019-05-09 13:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmapp', '0005_auto_20190509_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='cropexpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('to_give_whom', models.CharField(max_length=100)),
                ('crop_id', models.IntegerField()),
                ('expenses_name', models.TextField()),
                ('expenses_amount', models.FloatField()),
            ],
            options={
                'db_table': 'crop_expenses',
            },
        ),
        migrations.CreateModel(
            name='cropsold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('sold_to_whom', models.CharField(max_length=100)),
                ('crop_id', models.IntegerField()),
                ('sold', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'crop_sold',
            },
        ),
        migrations.RenameField(
            model_name='cropentry',
            old_name='year',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='cropentry',
            name='expenses_amount',
        ),
        migrations.RemoveField(
            model_name='cropentry',
            name='expenses_name',
        ),
        migrations.RemoveField(
            model_name='cropentry',
            name='sold',
        ),
    ]