# Generated by Django 5.0 on 2023-12-26 14:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lands", "0004_contact"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contact",
            options={"ordering": ["name"]},
        ),
    ]