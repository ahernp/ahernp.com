# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-08 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("pages", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="content",
            field=models.TextField(blank=True, verbose_name="Page content"),
        ),
        migrations.AlterField(
            model_name="page",
            name="content_type",
            field=models.CharField(
                choices=[
                    ("homepage", "Homepage"),
                    ("markdown", "Markdown"),
                    ("table", "Table"),
                ],
                default="markdown",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="page",
            name="published",
            field=models.DateField(
                blank=True,
                help_text="dd/mm/yyyy",
                null=True,
                verbose_name="Date Published",
            ),
        ),
    ]
