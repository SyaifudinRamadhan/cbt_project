# Generated by Django 3.2.7 on 2021-09-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminSide', '0003_result_test_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest_data',
            name='serial_quest',
            field=models.CharField(max_length=255),
        ),
    ]
