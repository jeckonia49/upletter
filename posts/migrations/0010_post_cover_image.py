# Generated by Django 5.0 on 2023-12-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0009_alter_postcomment_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="cover_image",
            field=models.ImageField(
                blank=True,
                help_text="for post detail banner",
                null=True,
                upload_to="cover/",
            ),
        ),
    ]