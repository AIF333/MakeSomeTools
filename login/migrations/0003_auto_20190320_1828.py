# Generated by Django 2.1.7 on 2019-03-20 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_login'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Login',
            new_name='User',
        ),
    ]
