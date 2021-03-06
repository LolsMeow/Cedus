# Generated by Django 3.2.8 on 2021-12-13 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20211210_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='Surgeries',
            fields=[
                ('surgery_id', models.AutoField(primary_key=True, serialize=False)),
                ('u_name', models.CharField(blank=True, max_length=50, null=True)),
                ('surgery_date', models.DateField()),
                ('surgery_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='provider',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
