# Generated by Django 3.2.8 on 2021-10-19 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_auto_20211019_0031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='user_cedus',
            name='phone_num',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user_cedus',
            name='role_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_id_U', to='patient.user_role'),
        ),
        migrations.AlterField(
            model_name='user_cedus',
            name='user_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='user_cedus',
            name='user_password',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user_role',
            name='role',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
