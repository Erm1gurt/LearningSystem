# Generated by Django 5.0.2 on 2024-03-02 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_alter_lessons_options_alter_user_is_teacher_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='price',
            field=models.BooleanField(choices=[(0, 'Свободный доступ'), (1, 'C оплатой')], default=0),
        ),
    ]
