from decimal import Decimal
from .categories import CATEGORY_CHOICES
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100, choices= CATEGORY_CHOICES)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(Decimal("0.0"))])
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    bids = models.ManyToManyField("Bid", related_name="listing_bids")
    winning_bid = models.ForeignKey("Bid", on_delete=models.SET_NULL, null=True, blank=True, related_name="winning_bid_listing")
    watchlist = models.ManyToManyField("Watchlist", related_name="watchlisted_by", blank=True)

    def __str__(self):
         return f"Title: {self.title}\nCategory: {self.category}\nSeller: {self.seller.first_name} {self.seller.last_name}\nStatus: {'Active' if self.is_active else 'Sold to ' + str(self.winning_bid.bidder) + ' at a price of ' + str(self.winning_bid.amount) +'$'}\n\n"


class Watchlist(models.Model):   
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   item = models.ManyToManyField(Listing, related_name="watchlists")
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return f"{self.user}'s watchlisted {self.item}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_listing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} bid by {self.bidder}"
    

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter} added a comment\n{self.comment}\n{self.created_at}\n\n"