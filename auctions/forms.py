from django import forms
from .models import *

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "starting_bid", "image_url"]
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
