# Generated by Django 5.0.1 on 2024-02-08 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0015_feedbackoption'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]