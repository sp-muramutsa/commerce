from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
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
                starting_bid = form.cleaned_data["starting_bid"],
                seller = request.user,
                image_url = form.cleaned_data["image_url"]
            )
            return redirect("index")
        
        else:
            return render(request, "auctions/list.html", {
                "form": ListingForm()
            })


    else:
        return render(request, "auctions/list.html", {
            "form": ListingForm()
        })


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    all_bids = Bid.objects.filter(listing=listing)
    min_to_bid = all_bids.aggregate(max_bid=Max('amount'))['max_bid'] or listing.starting_bid
    min_to_bid = round(min_to_bid, 1)
    on_watch = False
    ownership = False
    bid_status = False
    


    if request.user.is_authenticated:
        current_user = request.user
        listing_owner = listing.seller
        if current_user == listing_owner:
            ownership = True


        winning_bid = listing.winning_bid
        if winning_bid:
            bidder_winner = winning_bid.bidder
            if bidder_winner == current_user:
                bid_status = True

            

        user_watchlist, _ = Watchlist.objects.get_or_create(user=current_user)
        on_watch = listing in user_watchlist.item.all()

        if request.method == "POST":
            action = request.POST.get("action")

            if action == "add_to_watchlist":
                user_watchlist.item.add(listing)

            elif action == "remove_from_watchlist":
                user_watchlist.item.remove(listing)

            elif action == "bid":
                amount = float(request.POST.get("amount"))
                if amount <= min_to_bid:
                    error_message = f"Bid should be higher than the current highest bid of {round(min_to_bid, 1)}$"
                    return render(request, "auctions/listing.html", {
                        "bid_status": bid_status,
                        "error_message": error_message,
                        "listing": listing,
                        "min_to_bid": min_to_bid,
                        "on_watch": on_watch,
                        "ownership": ownership
                    })
                else:
                    bid = Bid.objects.create(listing=listing, bidder=current_user, amount=amount)
                    bid.save()
                return HttpResponseRedirect(request.path)
            
            elif action == "close":
                all_bids = Bid.objects.filter(listing=listing)
                if all_bids:
                    winner = all_bids.order_by('-amount').first()
                    listing.winning_bid = winner
                listing.is_active = False
                listing.save()
                
            
            
    elif request.method == "POST":
            # Redirect to the login page if the user tries to take further actions while not logged in
            return HttpResponseRedirect(reverse('login'))

    return render(request, "auctions/listing.html", {
        "bid_status": bid_status,
        "listing": listing,
        "min_to_bid": min_to_bid,
        "on_watch": on_watch,
        "ownership": ownership
    })