# Generated by Django 4.2.6 on 2023-10-14 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repository',
            name='avatar_url',
        ),
    ]