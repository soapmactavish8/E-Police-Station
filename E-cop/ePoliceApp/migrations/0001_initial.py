# Generated by Django 3.2.3 on 2021-06-28 05:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chowki',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ChID', models.CharField(default='', max_length=20)),
                ('Mobile', models.CharField(default='', max_length=10)),
                ('ChowkiName', models.CharField(max_length=50)),
                ('Address', models.TextField(default='', max_length=50)),
            ],
            options={
                'db_table': 'Chowki',
            },
        ),
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UID', models.CharField(max_length=20)),
                ('Image', models.FileField(default='avtar.jpg', upload_to='image/users/profile_pic/')),
                ('FullName', models.CharField(default='', max_length=50)),
                ('Mobile', models.CharField(default='', max_length=10)),
                ('Gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=50)),
                ('Address', models.TextField(default='', max_length=50)),
                ('Country', models.CharField(default='India', max_length=20)),
                ('State', models.CharField(default='', max_length=20)),
                ('City', models.CharField(default='', max_length=20)),
                ('Pincode', models.CharField(default='', max_length=6)),
            ],
            options={
                'db_table': 'Citizen',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'City',
            },
        ),
        migrations.CreateModel(
            name='CrimeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Crime', models.CharField(max_length=50)),
                ('Type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'CrimeList',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeptID', models.CharField(default='', max_length=20)),
                ('Image', models.FileField(default='avtar.jpg', upload_to='image/departments/profile_pic')),
                ('DeptName', models.CharField(default='', max_length=50)),
                ('Mobile', models.CharField(default='', max_length=10)),
                ('HeadOfficeAddress', models.CharField(default='', max_length=100)),
                ('About', models.CharField(default='', max_length=500)),
            ],
            options={
                'db_table': 'Department',
            },
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=50, unique=True)),
                ('Password', models.CharField(max_length=50)),
                ('IsActive', models.BooleanField(default=False)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateUpdated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Master',
            },
        ),
        migrations.CreateModel(
            name='PolicePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PoID', models.CharField(default='', max_length=20)),
                ('Image', models.FileField(default='avtar.jpg', upload_to='image/department/police_person/')),
                ('FullName', models.CharField(default='', max_length=50)),
                ('Mobile', models.CharField(default='', max_length=10)),
                ('Gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=50)),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.department')),
                ('Master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.master')),
            ],
            options={
                'db_table': 'PolicePerson',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Role',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Country', models.CharField(default='India', max_length=20)),
                ('Name', models.CharField(default='', max_length=20)),
            ],
            options={
                'db_table': 'State',
            },
        ),
        migrations.CreateModel(
            name='SuspectList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.FileField(default='avtar.jpg', upload_to='image/users/suspects/')),
                ('SuspectName', models.CharField(max_length=50)),
                ('SuspectMobile', models.CharField(max_length=10, null=True)),
                ('Gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=50)),
                ('SuspectAddress', models.TextField(max_length=200)),
                ('Citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.citizen')),
            ],
            options={
                'db_table': 'SuspectList',
            },
        ),
        migrations.CreateModel(
            name='SubInspector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Chowki', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.chowki')),
                ('PolicePerson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.policeperson')),
            ],
            options={
                'db_table': 'SubInspector',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StID', models.CharField(default='', max_length=20)),
                ('StationName', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=50, unique=True)),
                ('Mobile', models.CharField(default='', max_length=10)),
                ('Address', models.TextField(default='', max_length=50)),
                ('Pincode', models.CharField(default='', max_length=6)),
                ('City', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.city')),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.department')),
            ],
            options={
                'db_table': 'Station',
            },
        ),
        migrations.AddField(
            model_name='master',
            name='Role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.role'),
        ),
        migrations.CreateModel(
            name='Inspector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PolicePerson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.policeperson')),
                ('Station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.station')),
            ],
            options={
                'db_table': 'Inspector',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='Master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.master'),
        ),
        migrations.AddField(
            model_name='department',
            name='State',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.state'),
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ComplaintID', models.CharField(max_length=12)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateOfCrime', models.DateField(default=datetime.datetime(2021, 6, 28, 11, 0, 19, 598107))),
                ('Description', models.TextField(max_length=500)),
                ('Chowki', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.chowki')),
                ('Citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.citizen')),
                ('CrimeList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.crimelist')),
                ('SuspectList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.suspectlist')),
            ],
            options={
                'db_table': 'Complaint',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='State',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.state'),
        ),
        migrations.AddField(
            model_name='citizen',
            name='Master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.master'),
        ),
        migrations.AddField(
            model_name='chowki',
            name='Station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ePoliceApp.station'),
        ),
    ]
