# Generated by Django 5.0.3 on 2024-05-07 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_alter_listing_watchlist"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="price",
        ),
    ]
