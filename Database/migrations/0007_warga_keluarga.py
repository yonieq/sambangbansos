# Generated by Django 3.0.6 on 2020-06-04 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0006_auto_20200604_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='warga',
            name='Keluarga',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Database.Keluarga'),
        ),
    ]
