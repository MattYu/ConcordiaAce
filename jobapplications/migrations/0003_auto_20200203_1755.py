# Generated by Django 3.0 on 2020-02-03 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('jobapplications', '0002_auto_20200203_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='candidate',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='accounts.Candidate'),
        ),
    ]
