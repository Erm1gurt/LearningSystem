# Generated by Django 5.0.2 on 2024-03-02 23:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_groups_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.AlterModelOptions(
            name='groups',
            options={'ordering': ['-title']},
        ),
        migrations.AddIndex(
            model_name='groups',
            index=models.Index(fields=['-title'], name='mainapp_gro_title_3be6b5_idx'),
        ),
        migrations.AddField(
            model_name='customers',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.courses'),
        ),
        migrations.AddField(
            model_name='customers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]