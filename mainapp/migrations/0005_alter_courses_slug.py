# Generated by Django 5.0.2 on 2024-03-01 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_courses_time_start_lessons_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='slug',
            field=models.SlugField(default=None, unique=True),
        ),
    ]
