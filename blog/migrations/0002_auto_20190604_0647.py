# Generated by Django 2.2.2 on 2019-06-04 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpage',
            options={'ordering': ['-published']},
        ),
    ]
