# Generated by Django 2.1.3 on 2018-12-14 11:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta", "0002_auto_20181130_1141"),
    ]

    operations = [
        migrations.AddField(
            model_name="source",
            name="meta_data",
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
