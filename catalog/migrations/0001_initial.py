# Generated by Django 3.1.6 on 2021-02-04 11:55

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataLoad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full', models.ImageField(upload_to=catalog.models.get_image_path)),
                ('thumbnails', models.ImageField(upload_to=catalog.models.get_image_path)),
                ('large', models.ImageField(upload_to=catalog.models.get_image_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('methods', models.ManyToManyField(related_name='doctors', to='catalog.Method')),
                ('photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='catalog.photo')),
            ],
        ),
    ]
