# Generated by Django 4.1 on 2022-09-13 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_product_highlight1_product_highlight2_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="covered_in",
            field=models.CharField(
                blank=True, default="Manufacturing Defects", max_length=50, null=True
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="domestic_war",
            field=models.CharField(
                blank=True, default="1 Year", max_length=50, null=True
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="not_covered_in",
            field=models.CharField(
                blank=True, default="Physical Damage", max_length=50, null=True
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="war_service_type",
            field=models.CharField(
                blank=True, default="Onsite", max_length=50, null=True
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="war_summary",
            field=models.CharField(
                blank=True, default="1 Year Onsite Warranty", max_length=50, null=True
            ),
        ),
    ]
