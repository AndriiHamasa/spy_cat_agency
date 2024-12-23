# Generated by Django 5.1.3 on 2024-11-26 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agency", "0004_rename_is_completed_mission_mission_completed_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="cat",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Missions",
                to="agency.cat",
            ),
        ),
    ]
