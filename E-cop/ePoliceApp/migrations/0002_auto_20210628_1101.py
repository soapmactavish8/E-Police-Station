# Generated by Django 3.2.3 on 2021-06-28 05:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ePoliceApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='Chowki',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='Citizen',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='CrimeList',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='SuspectList',
        ),
        migrations.AlterField(
            model_name='complaint',
            name='DateOfCrime',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 11, 1, 25, 513838)),
        ),
    ]
