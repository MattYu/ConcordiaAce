# Generated by Django 3.0 on 2020-02-03 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('joblistings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=40)),
                ('lastName', models.CharField(default='', max_length=40)),
                ('preferredName', models.CharField(default='', max_length=40)),
                ('status', models.CharField(choices=[('Pending', 'Pending Coop Review'), ('Submitted', 'Submitted to Employer'), ('Interviewing', 'Selected for Interview'), ('Not Selected', 'Not Selected'), ('Ranked', 'Ranked by Employer'), ('Matched', 'Matched'), ('Not Matched', 'Not Matched'), ('Closed', 'Closed')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('candidate', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='joblistings.Job')),
            ],
        ),
        migrations.CreateModel(
            name='SupportingDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(default='', max_length=40)),
                ('document', models.FileField(default='', upload_to='user/document/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('JobApplication', models.ManyToManyField(to='jobapplications.JobApplication')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(default='', max_length=40)),
                ('resume', models.FileField(default='', upload_to='user/resume/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('JobApplication', models.ManyToManyField(to='jobapplications.JobApplication')),
            ],
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employerRank', models.IntegerField(default=1000)),
                ('userRank', models.IntegerField(default=1000)),
                ('preferredName', models.CharField(default='', max_length=40)),
                ('status', models.CharField(choices=[('Pending', 'Pending Coop Review'), ('Submitted', 'Submitted to Employer'), ('Interviewing', 'Selected for Interview'), ('Not Selected', 'Not Selected'), ('Ranked', 'Ranked by Employer'), ('Matched', 'Matched'), ('Not Matched', 'Not Matched'), ('Closed', 'Closed')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('candidate', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='joblistings.Job')),
                ('jobApplication', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='jobapplications.JobApplication')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(default='', max_length=40)),
                ('title', models.CharField(default='', max_length=40)),
                ('period', models.CharField(default='', max_length=40)),
                ('description', tinymce.models.HTMLField(default='', max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('JobApplication', models.ManyToManyField(to='jobapplications.JobApplication')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.CharField(default='', max_length=40)),
                ('title', models.CharField(default='', max_length=40)),
                ('period', models.CharField(default='', max_length=40)),
                ('description', tinymce.models.HTMLField(default='', max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('JobApplication', models.ManyToManyField(to='jobapplications.JobApplication')),
            ],
        ),
        migrations.CreateModel(
            name='CoverLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(default='', max_length=40)),
                ('coverLetter', models.FileField(default='', upload_to='user/coverletter/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('JobApplication', models.ManyToManyField(to='jobapplications.JobApplication')),
            ],
        ),
    ]
