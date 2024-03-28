# Generated by Django 5.0.1 on 2024-03-26 08:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_questionnairequestions_alter_appointment_time_slot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time_slot',
            field=models.TimeField(choices=[(datetime.time(9, 0), '09:00 AM'), (datetime.time(11, 0), '11:00 AM'), (datetime.time(13, 0), '01:00 PM'), (datetime.time(15, 0), '03:00 PM'), (datetime.time(17, 0), '05:00 PM')], null=True),
        ),
    ]
