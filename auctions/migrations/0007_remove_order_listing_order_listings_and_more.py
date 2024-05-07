# Generated by Django 5.0.3 on 2024-05-07 03:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_listing_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="listing",
        ),
        migrations.AddField(
            model_name="order",
            name="listings",
            field=models.ManyToManyField(
                related_name="custom_orders", to="auctions.listing"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="orders",
            field=models.ManyToManyField(
                related_name="custom_listings", to="auctions.order"
            ),
        ),
        migrations.CreateModel(
            name="Watchlist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("item", models.ManyToManyField(to="auctions.listing")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]