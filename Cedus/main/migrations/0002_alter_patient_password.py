# Generated by Django 3.2.8 on 2021-10-22 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
