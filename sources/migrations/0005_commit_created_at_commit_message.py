# Generated by Django 4.2.6 on 2023-10-15 09:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0004_rename_hash_commit_sha'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commit',
            name='message',
            field=models.TextField(default='Hello'),
            preserve_default=False,
        ),
    ]
