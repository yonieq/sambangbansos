# Generated by Django 3.2.4 on 2021-07-15 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0019_alter_usulan_nik'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usulan',
            options={'ordering': ('NomerKK',)},
        ),
    ]
