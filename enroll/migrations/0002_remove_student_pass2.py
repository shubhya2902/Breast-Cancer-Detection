# Generated by Django 5.1.6 on 2025-02-07 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='pass2',
        ),
    ]
