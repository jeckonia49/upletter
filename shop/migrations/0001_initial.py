# Generated by Django 5.0 on 2023-12-27 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0010_alter_sociallink_platform"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shop",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "cover_image",
                    models.ImageField(blank=True, null=True, upload_to="shop/"),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "vendor",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_shop",
                        to="accounts.profile",
                    ),
                ),
            ],
        ),
    ]
