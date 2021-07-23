# Generated by Django 3.2.4 on 2021-07-15 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0020_alter_usulan_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usulan',
            options={},
        ),
        migrations.AlterField(
            model_name='usulan',
            name='Nik',
            field=models.CharField(max_length=17),
        ),
        migrations.AlterField(
            model_name='usulan',
            name='Status',
            field=models.CharField(choices=[('0', 'Usulan'), ('1', 'Disetujui')], default='0', max_length=1),
        ),
    ]