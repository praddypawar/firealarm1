# Generated by Django 3.1.5 on 2022-06-04 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20220604_2027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devices',
            options={'ordering': ['-id']},
        ),
    ]