# Generated by Django 2.1 on 2018-12-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("feedreader", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="entry",
            name="media_link",
            field=models.CharField(blank=True, max_length=2000, null=True),
        )
    ]
