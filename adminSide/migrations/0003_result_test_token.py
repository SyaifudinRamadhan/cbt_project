# Generated by Django 3.2.7 on 2021-09-20 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminSide', '0002_result_test_state_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='result_test',
            name='token',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
