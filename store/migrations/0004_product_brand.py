# Generated by Django 4.1 on 2022-09-12 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_product_specifications"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
