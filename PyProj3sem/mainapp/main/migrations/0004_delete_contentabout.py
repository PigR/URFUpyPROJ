# Generated by Django 4.0.5 on 2023-01-09 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_contentabout_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContentAbout',
        ),
    ]