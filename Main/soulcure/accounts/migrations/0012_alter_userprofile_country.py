# Generated by Django 4.2.4 on 2023-09-10 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_userprofile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, choices=[('India', 'India')], default='India', max_length=50, null=True),
        ),
    ]
