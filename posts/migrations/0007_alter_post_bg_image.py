# Generated by Django 5.0 on 2023-12-26 09:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0006_alter_post_editor_choice_postimageslide"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="bg_image",
            field=models.ImageField(upload_to="posts/"),
        ),
    ]