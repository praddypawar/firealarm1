# Generated by Django 3.1.5 on 2022-05-28 12:46

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20220528_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='system', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.PositiveIntegerField(choices=[(0, 'inactive'), (1, 'active'), (2, 'deleted_by_owner')], default=1)),
                ('cover_pic', models.ImageField(upload_to=api.models.set_cover_pic)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
