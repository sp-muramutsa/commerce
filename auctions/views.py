from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, path
from django import forms
from .forms import ListingForm
from .models import *

def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(first_name, last_name, username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def list(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.create(
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                category = form.cleaned_data["category"],
                price = form.cleaned_data["price"],
                starting_bid = form.cleaned_data["starting_bid"],
                seller = request.user,
                image_url = form.cleaned_data["image_url"]
            )
            return redirect("index")

    else:
        form = ListingForm()
        return render(request, "auctions/list.html", {
            "form": form
        })


def listing(request, listing_id):
    current_user = request.user
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "GET": 
         # Retrieve the user's watchlist
        user_watchlist, created = Watchlist.objects.get_or_create(user=current_user)

        # Check if the listing is in the user's watchlist
        on_watch = listing in user_watchlist.item.all()

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "on_watch": on_watch
            })
    
    elif request.method== "POST":
        action = request.POST.get("action")
        user_watchlist, created = Watchlist.objects.get_or_create(user=current_user)

        if action == "add_to_watchlist":
            user_watchlist.item.add(listing)
        
        elif action == "remove_from_watchlist":
            user_watchlist.item.remove(listing)
        
        return HttpResponseRedirect(request.path)
        
    else:
        return redirect("index")







    


   
