# Generated by Django 5.0 on 2023-12-26 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("flatpages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutFlatPage",
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
                (
                    "cover_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="flatpages/contact/"
                    ),
                ),
                (
                    "page",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="about_flatepage",
                        to="flatpages.flatpage",
                    ),
                ),
            ],
            options={
                "verbose_name": "About FlatPage",
                "verbose_name_plural": "About FlatPages",
            },
        ),
        migrations.CreateModel(
            name="ContactFlatPage",
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
                ("address", models.CharField(max_length=100)),
                (
                    "phone",
                    models.CharField(
                        help_text="phone number startting with the country code i.e 2447(123)987654",
                        max_length=100,
                    ),
                ),
                (
                    "mail",
                    models.EmailField(help_text="gmagnews@domain.com", max_length=255),
                ),
                (
                    "cover_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="flatpages/contact/"
                    ),
                ),
                (
                    "page",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="contact_flatepage",
                        to="flatpages.flatpage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Contact FlatPage",
                "verbose_name_plural": "Contact FlatPages",
            },
        ),
    ]