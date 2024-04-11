from .categories import CATEGORY_CHOICES
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    address = models.ForeignKey("Address", on_delete=models.PROTECT, null=True)
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100, choices= CATEGORY_CHOICES)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    bids = models.ManyToManyField("Bid", related_name="listings")
    orders = models.ManyToManyField("Order", related_name="listings")

    def __str__(self):
        return f"Title: {self.title}\nCategory: {self.category}\nSeller: {self.seller.first_name} {self.seller.last_name}\nStatus: {'Active' if self.is_active else 'Sold'}\n\n"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} bid by {self.bidder}"

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} units, bought by {self.buyer}, for a total of {self.total_price}"

class Comment(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment}"


class Address(models.Model):
    country = models.CharField(max_length=100, null=False)
    street_address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.country} - {self.zip_code}"

