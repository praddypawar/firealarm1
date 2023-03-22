# Generated by Django 3.1.5 on 2022-05-31 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='devices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='system', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.PositiveIntegerField(choices=[(0, 'inactive'), (1, 'active'), (2, 'deleted_by_owner')], default=1)),
                ('name', models.CharField(max_length=255)),
                ('device_id', models.CharField(max_length=255)),
                ('device_status', models.CharField(choices=[('on', 'on'), ('off', 'off')], default='off', max_length=100)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.admins')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
