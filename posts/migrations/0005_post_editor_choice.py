# Generated by Django 5.0 on 2023-12-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0004_post_comments"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="editor_choice",
            field=models.BooleanField(default=True),
        ),
    ]