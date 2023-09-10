# Generated by Django 4.2.4 on 2023-09-09 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, choices=[('Afghanistan', 'Afghanistan'), ('Armenia', 'Armenia'), ('Azerbaijan', 'Azerbaijan'), ('Bahrain', 'Bahrain'), ('Bangladesh', 'Bangladesh'), ('Bhutan', 'Bhutan'), ('Brunei', 'Brunei'), ('Cambodia', 'Cambodia'), ('China', 'China'), ('Cyprus', 'Cyprus'), ('Georgia', 'Georgia'), ('India', 'India'), ('Indonesia', 'Indonesia'), ('Iran', 'Iran'), ('Iraq', 'Iraq'), ('Israel', 'Israel'), ('Japan', 'Japan'), ('Jordan', 'Jordan'), ('Kazakhstan', 'Kazakhstan'), ('Kuwait', 'Kuwait'), ('Kyrgyzstan', 'Kyrgyzstan'), ('Laos', 'Laos'), ('Lebanon', 'Lebanon'), ('Malaysia', 'Malaysia'), ('Maldives', 'Maldives'), ('Mongolia', 'Mongolia'), ('Myanmar (Burma)', 'Myanmar (Burma)'), ('Nepal', 'Nepal'), ('North Korea', 'North Korea'), ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Palestine', 'Palestine'), ('Philippines', 'Philippines'), ('Qatar', 'Qatar'), ('Saudi Arabia', 'Saudi Arabia'), ('Singapore', 'Singapore'), ('South Korea', 'South Korea'), ('Sri Lanka', 'Sri Lanka'), ('Syria', 'Syria'), ('Tajikistan', 'Tajikistan'), ('Thailand', 'Thailand'), ('Timor-Leste', 'Timor-Leste'), ('Turkey', 'Turkey'), ('Turkmenistan', 'Turkmenistan'), ('United Arab Emirates', 'United Arab Emirates'), ('Uzbekistan', 'Uzbekistan'), ('Vietnam', 'Vietnam'), ('Yemen', 'Yemen')], default='India', max_length=50, null=True),
        ),
    ]
