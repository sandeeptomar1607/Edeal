# Generated by Django 4.1 on 2022-09-16 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0009_coupon_bank_coupon_brand_coupon_category_coupon_min_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="bank",
            field=models.CharField(blank=True, default=None, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="brand",
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="category",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.category",
            ),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="min",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="product",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.product",
            ),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="sub_cat",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.subcategory",
            ),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="upto",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]