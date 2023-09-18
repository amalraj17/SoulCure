# Generated by Django 4.2.4 on 2023-09-17 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_appointment_modified_date_alter_appointment_status'),
        ('therapist', '0008_alter_therapist_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=100)),
                ('meeting_url', models.URLField()),
                ('scheduled_time', models.DateTimeField()),
                ('duration_minutes', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed')], default='scheduled', max_length=20)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.appointment')),
            ],
        ),
    ]
