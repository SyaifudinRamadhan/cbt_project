# Generated by Django 3.2.7 on 2021-09-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='class_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=30)),
                ('id_teacher', models.CharField(max_length=20)),
                ('id_admin', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='course_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=40)),
                ('id_teacher', models.CharField(max_length=20)),
                ('id_admin', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='quest_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_quest', models.CharField(max_length=20)),
                ('id_teacher', models.CharField(max_length=20)),
                ('id_course', models.IntegerField()),
                ('id_admin', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='result_test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('result', models.FloatField()),
                ('id_quest', models.IntegerField()),
                ('id_students', models.CharField(max_length=20)),
                ('id_admin', models.IntegerField()),
                ('id_teacher', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='schedule_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('duration', models.IntegerField()),
                ('state', models.CharField(max_length=10)),
                ('id_teacher', models.CharField(max_length=20)),
                ('id_class', models.IntegerField()),
                ('id_course', models.IntegerField()),
                ('id_admin', models.IntegerField()),
                ('token', models.CharField(max_length=10)),
            ],
        ),
    ]
