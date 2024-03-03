# Generated by Django 5.0.2 on 2024-03-01 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_courses_slug_courses_time_update_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='time_start',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='lessons',
            name='video',
            field=models.URLField(default=None),
        ),
    ]
