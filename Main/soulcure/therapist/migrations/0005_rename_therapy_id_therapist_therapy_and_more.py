# Generated by Django 4.2.4 on 2023-08-16 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0004_therapist_userprofile_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='therapist',
            old_name='therapy_id',
            new_name='therapy',
        ),
        migrations.RenameField(
            model_name='therapist',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='therapist',
            old_name='userprofile_id',
            new_name='user_profile',
        ),
    ]
