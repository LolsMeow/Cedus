# Generated by Django 3.2.8 on 2021-10-21 23:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('birth_date', models.DateField(default=datetime.date.today)),
                ('phone_number', models.CharField(max_length=50)),
                ('street_address', models.CharField(max_length=50)),
                ('apt', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.IntegerField(blank=True, null=True)),
                ('provider_name', models.CharField(max_length=50)),
                ('plan_name', models.CharField(max_length=50)),
                ('rx_bin', models.IntegerField(blank=True, null=True)),
                ('id_number', models.IntegerField(blank=True, null=True)),
                ('rx_pcn', models.IntegerField(blank=True, null=True)),
                ('rx_group', models.CharField(max_length=50)),
            ],
        ),
    ]