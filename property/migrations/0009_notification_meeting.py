# Generated by Django 5.0.6 on 2024-05-25 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0008_meeting"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="meeting",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="property.meeting",
            ),
        ),
    ]
