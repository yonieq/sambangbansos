# Generated by Django 3.0.6 on 2020-06-04 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0004_auto_20200604_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='penduduk',
            name='Nik',
            field=models.CharField(default='', max_length=17),
        ),
        migrations.AlterField(
            model_name='keluarga',
            name='NomerKK',
            field=models.CharField(max_length=17, unique=True),
        ),
    ]
