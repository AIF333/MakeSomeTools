# Generated by Django 2.1.7 on 2019-03-20 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResManage',
            fields=[
                ('resid', models.AutoField(primary_key=True, serialize=False)),
                ('resname', models.CharField(max_length=32)),
                ('resip', models.CharField(max_length=32)),
            ],
        ),
    ]
