# Generated by Django 3.2.4 on 2021-07-15 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0022_auto_20210715_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='warga',
            name='Status',
            field=models.CharField(choices=[('0', 'Usulan'), ('1', 'Disetujui')], default='0', max_length=1),
        ),
        migrations.DeleteModel(
            name='Usulan',
        ),
    ]
