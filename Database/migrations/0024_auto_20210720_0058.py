# Generated by Django 2.2.10 on 2021-07-19 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0023_auto_20210715_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warga',
            name='Status',
            field=models.CharField(choices=[('Usulan', 'Usulan'), ('Disetujui', 'Disetujui')], default='usulan', max_length=10),
        ),
    ]
