# Generated by Django 5.0 on 2023-12-26 20:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0012_alter_post_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(),
        ),
    ]
