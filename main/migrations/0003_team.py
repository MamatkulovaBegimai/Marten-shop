# Generated by Django 5.1.4 on 2025-01-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_aboutus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='team_photo/', verbose_name='Фотография')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('job_title', models.CharField(max_length=100, verbose_name='Должность')),
                ('instagram', models.URLField(verbose_name='Инстаграм')),
                ('facebook', models.URLField(verbose_name='Фейсбук')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Сотрудник',
            },
        ),
    ]
