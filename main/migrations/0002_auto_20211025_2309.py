# Generated by Django 3.2.8 on 2021-10-26 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergies',
            name='aller_drug',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='ins_rx_group',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]