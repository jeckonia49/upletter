# Generated by Django 5.0 on 2023-12-31 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_alter_sociallink_platform"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="skills",
            field=models.CharField(
                blank=True,
                help_text="if multiple skills, separate with commas",
                max_length=300,
                null=True,
            ),
        ),
    ]
