# Generated by Django 4.0.5 on 2023-01-10 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_tablesalaryyear_delete_tables_alter_charts_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TablesМacanciesYears',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(verbose_name='Год')),
                ('vacanсies', models.PositiveIntegerField(verbose_name='Год')),
            ],
            options={
                'verbose_name': 'Строку',
                'verbose_name_plural': 'Динамика кол-ва вакансий по годам',
            },
        ),
    ]
