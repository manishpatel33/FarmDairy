# Generated by Django 2.2.1 on 2019-05-03 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='farmuser',
            old_name='mobile_no',
            new_name='contact_no',
        ),
        migrations.RenameField(
            model_name='farmuser',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='farmuser',
            name='last_name',
        ),
    ]
