# Generated by Django 3.2.8 on 2021-10-19 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20211018_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='user_id',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_id_P', to='patient.user_cedus'),
        ),
    ]
