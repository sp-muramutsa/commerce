# Generated by Django 5.0.3 on 2024-04-11 02:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("country", models.CharField(max_length=100)),
                ("street_address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("zip_code", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Electronics", "Electronics"),
                            ("Books", "Books"),
                            ("Clothing", "Clothing"),
                            ("Home and Garden", "Home and Garden"),
                            ("Toys and Games", "Toys and Games"),
                            ("Beauty and Health", "Beauty and Health"),
                            ("Sports and Outdoors", "Sports and Outdoors"),
                            ("Other", "Other"),
                        ],
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="date_of_birth",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="auctions.address",
            ),
        ),
        migrations.CreateModel(
            name="Bid",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "bidder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bidders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "commenter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commenters",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Listing",
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
                ("title", models.CharField(max_length=30)),
                ("description", models.TextField()),
                ("starting_bid", models.DecimalField(decimal_places=2, max_digits=10)),
                ("image_url", models.URLField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "bids",
                    models.ManyToManyField(related_name="listings", to="auctions.bid"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="auctions.category",
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="bid",
            name="listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="auctions.listing"
            ),
        ),
        migrations.CreateModel(
            name="Order",
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
                ("quantity", models.PositiveIntegerField(default=1)),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "listing",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auctions.listing",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="listing",
            name="orders",
            field=models.ManyToManyField(related_name="listings", to="auctions.order"),
        ),
    ]