# Generated by Django 4.1 on 2022-09-16 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="valid_till",
            field=models.DateField(default=None),
        ),
    ]
