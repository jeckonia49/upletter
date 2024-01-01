# Generated by Django 5.0 on 2024-01-01 05:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0011_profile_skills"),
        ("posts", "0018_video"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdministratorPostSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_viewed", models.BooleanField(default=False)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_profile_session_data",
                        to="posts.post",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_session_data",
                        to="accounts.profile",
                    ),
                ),
            ],
        ),
    ]