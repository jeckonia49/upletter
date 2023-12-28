# Generated by Django 5.0 on 2023-12-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0006_shopproductdetailview_rename_count_cart_item_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="selling_price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="ShopProductDetailView",
        ),
    ]