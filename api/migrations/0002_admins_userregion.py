# Generated by Django 3.1.5 on 2022-05-28 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admins',
            name='userRegion',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]