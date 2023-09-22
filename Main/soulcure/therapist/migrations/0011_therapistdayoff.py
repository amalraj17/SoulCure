# Generated by Django 4.2.4 on 2023-09-21 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0010_leaverequest_delete_meeting'),
    ]

    operations = [
        migrations.CreateModel(
            name='TherapistDayOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='therapist.therapist')),
            ],
        ),
    ]