# Generated by Django 3.0 on 2020-03-17 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmatchings', '0003_match_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchinghistory',
            name='isOpenToPublic',
            field=models.BooleanField(default=False),
        ),
    ]
