# Generated by Django 4.2.4 on 2023-08-16 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_role'),
        ('therapist', '0003_remove_therapist_userprofile_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapist',
            name='userprofile_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
        ),
    ]
