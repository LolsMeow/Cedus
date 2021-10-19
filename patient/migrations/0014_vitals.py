# Generated by Django 3.2.8 on 2021-10-19 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_allergies'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vitals',
            fields=[
                ('vt_no', models.IntegerField(primary_key=True, serialize=False)),
                ('vt_date', models.DateField()),
                ('vt_bloodgroup', models.CharField(max_length=100)),
                ('vt_bp_sys', models.IntegerField()),
                ('vt_bp_dia', models.IntegerField()),
                ('vt_wbc', models.IntegerField()),
                ('vt_rbc', models.IntegerField()),
                ('vt_height', models.DecimalField(decimal_places=2, max_digits=3)),
                ('vt_weight', models.DecimalField(decimal_places=2, max_digits=4)),
                ('vt_comments', models.CharField(max_length=100)),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
            ],
        ),
    ]
