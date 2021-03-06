# Generated by Django 2.1.7 on 2019-05-12 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('roomid', models.CharField(max_length=100)),
                ('history', models.CharField(max_length=5000)),
                ('cmd', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=20)),
                ('lastTime', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('room', models.CharField(max_length=100)),
                ('score', models.CharField(max_length=20)),
                ('act', models.CharField(max_length=40)),
                ('status', models.CharField(max_length=10)),
                ('useScript', models.CharField(max_length=5)),
            ],
        ),
    ]
