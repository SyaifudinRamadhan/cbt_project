# Generated by Django 3.2.7 on 2021-09-10 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='students_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_induk', models.CharField(max_length=20)),
                ('guru_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='theachers_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_induk', models.CharField(max_length=20)),
                ('agency', models.CharField(max_length=50)),
                ('admin_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='user_second',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_induk', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=10)),
            ],
        ),
    ]
