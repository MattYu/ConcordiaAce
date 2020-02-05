# Generated by Django 3.0 on 2020-02-05 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapplications', '0005_auto_20200204_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(choices=[('Pending Review', 'Pending Coop Review'), ('Not Approved', 'Not Approved'), ('Submitted', 'Submitted to Employer'), ('Interviewing', 'Selected for Interview'), ('Not Selected', 'Not Selected'), ('Ranked', 'Ranked by Employer'), ('Matched', 'Matched'), ('Not Matched', 'Not Matched'), ('Closed', 'Closed')], default='Pending Review', max_length=20),
        ),
    ]