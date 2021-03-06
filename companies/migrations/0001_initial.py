# Generated by Django 3.0 on 2020-02-03 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('website', models.CharField(default='', max_length=100)),
                ('profile', models.TextField(default='', max_length=1000)),
                ('image', models.ImageField(default='images/company/company-logo-1', upload_to='images/company/')),
                ('status', models.CharField(choices=[('Pending', 'Pending Coop Review'), ('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Pending', max_length=20)),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
    ]
