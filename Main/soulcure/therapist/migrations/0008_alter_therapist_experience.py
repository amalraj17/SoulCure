# Generated by Django 4.2.4 on 2023-09-04 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0007_alter_therapist_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='experience',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
