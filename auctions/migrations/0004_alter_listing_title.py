# Generated by Django 5.0.3 on 2024-04-11 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_listing_category_delete_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="title",
            field=models.CharField(max_length=100),
        ),
    ]
