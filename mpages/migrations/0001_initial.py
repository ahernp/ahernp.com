# Generated by Django 2.0.5 on 2018-06-09 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=250)),
                ("slug", models.SlugField(max_length=250, unique=True)),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Time Updated"),
                ),
                ("content", models.TextField(blank=True, verbose_name="Page content")),
                (
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="mpages.Page",
                    ),
                ),
            ],
            options={"ordering": ["title"]},
        )
    ]
