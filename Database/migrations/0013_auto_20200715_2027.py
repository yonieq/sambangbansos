# Generated by Django 3.0.7 on 2020-07-15 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0012_auto_20200715_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desa',
            name='Kode',
            field=models.CharField(db_index=True, max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='kecamatan',
            name='Kode',
            field=models.CharField(db_index=True, max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='warga',
            name='NikValid',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]