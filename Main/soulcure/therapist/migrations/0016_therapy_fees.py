# Generated by Django 4.2.4 on 2023-09-25 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0015_alter_therapysessionschedule_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapy',
            name='fees',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
