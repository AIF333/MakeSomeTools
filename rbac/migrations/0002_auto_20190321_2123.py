# Generated by Django 2.1.7 on 2019-03-21 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='promisions',
            new_name='permissions',
        ),
    ]
