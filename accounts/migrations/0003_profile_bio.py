# Generated by Django 5.0 on 2023-12-25 04:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_profile_first_name_profile_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(
                default="In a professional context it often happens that private or corporate clients corder a publication to be made and presented with the actual content still not being ready. Think of a news blog that’s filled with content hourly on the day of going live.",
                max_length=5000,
            ),
            preserve_default=False,
        ),
    ]
