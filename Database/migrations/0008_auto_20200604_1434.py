# Generated by Django 3.0.6 on 2020-06-04 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0007_warga_keluarga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warga',
            name='Nik',
            field=models.CharField(default='', max_length=17, unique=True),
        ),
    ]
