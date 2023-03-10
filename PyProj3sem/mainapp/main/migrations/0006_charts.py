# Generated by Django 4.0.5 on 2023-01-09 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название')),
                ('chart', models.ImageField(upload_to='images/charts')),
            ],
            options={
                'verbose_name': 'График',
                'verbose_name_plural': 'Графики',
            },
        ),
    ]
