# Generated by Django 3.0 on 2020-01-22 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('joblistings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPDFDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptionFile', models.FileField(default='', upload_to='company/jobDescription.')),
                ('job', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='joblistings.Job')),
            ],
        ),
    ]