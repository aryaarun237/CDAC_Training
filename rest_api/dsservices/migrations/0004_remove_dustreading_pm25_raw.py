# Generated by Django 5.2.3 on 2025-07-10 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dsservices', '0003_dustreading_pm25_raw'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dustreading',
            name='pm25_raw',
        ),
    ]
