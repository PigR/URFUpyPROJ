# Generated by Django 4.0.5 on 2023-01-09 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_delete_testt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentabout',
            name='image',
        ),
    ]