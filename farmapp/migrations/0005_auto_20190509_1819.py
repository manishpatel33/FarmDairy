# Generated by Django 2.2.1 on 2019-05-09 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmapp', '0004_auto_20190509_1751'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='entry',
            new_name='cropentry',
        ),
    ]