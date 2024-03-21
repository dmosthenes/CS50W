from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms import ModelForm, TextInput, Select, ModelChoiceField

from .models import User, Listing, Bids, Comments, Category

from datetime import datetime


class new_listing(ModelForm):

    category = ModelChoiceField(queryset=Category.objects.all(), empty_label="Select category", widget=Select(attrs={'class': 'form-control'}))
  
    class Meta:
        model = Listing
        fields = ['title','description','imageURL','duration', 'category', 'starting_price']
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            'description': TextInput(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'imageURL': TextInput(attrs={'placeholder': 'Enter image URL', 'class': 'form-control'}),
            'duration': TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': '1', 'min': '1', 'max': '7', 'placeholder': 'Enter duration in days'}),
            'starting_price': TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.01', 'placeholder': 'Starting Price'})
        }

class new_bid(ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']
        widgets = {
            'amount': TextInput(attrs={'placeholder': 'Amount', 'class': 'form-control'}),
            
        }

class new_comment(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': TextInput(attrs={'placeholder': 'Your comment here.', 'class': 'form-control'})
        }


def index(request):

    listings = Listing.objects.all()


    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def watchlist(request):

    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })


def add_to_watchlist(request, listing_id):

    # Add the listing of listing_id to watchlist

    lst = get_object_or_404(Listing, pk=listing_id)

    user = request.user

    user.watchlist.add(lst)
    
    return redirect('listing', listing_id)

def create_listing(request):

    if request.method == "POST":

        # Put form content into database
        form = new_listing(request.POST)

        # print(form.is_valid())
        
        if form.is_valid():

            user = request.user

            instance = form.save(commit=False)
            instance.seller = user

            instance.start = datetime.now()

            instance.save()

            id = instance.id
        
            return redirect('listing', id)

    return render(request, "auctions/create_listing.html", {
            "form": new_listing
        
    })


def listing(request, listing_id):

    lst = get_object_or_404(Listing, pk=listing_id)

    bid_warning = False

    if request.method == "POST":

        # Bids form
        if request.POST.get("form_name") == "bids":

            form = new_bid(request.POST)
            if form.is_valid():

                # Check that new bid is higher than starting price
                if int(form.cleaned_data["amount"]) >= int(lst.starting_price):

                    # Check that new bid is greater than previous or if there are no bids
                    bids = Bids.objects.filter(listing=lst).order_by("amount")
                    prev = bids[len(bids) -1] if bids else None

                    if not prev or int(form.cleaned_data["amount"]) > int(prev.amount):

                        print("adding bid")

                        bidder = request.user

                        instance = form.save(commit=False)
                        instance.bidder = bidder
                        instance.time = datetime.now()
                        instance.listing = lst

                        instance.save()

                    else:
                        bid_warning = True

                else:
                    bid_warning = True

        # Comments form
        else:

            form = new_comment(request.POST)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.commenter = request.user
                instance.time = datetime.now()
                instance.listing = lst

                instance.save()

    # Get the current high bid for the listing
    high_bid = None
    if Bids.objects.filter(listing=lst).exists():
        # high_bid = Bids.objects.filter(id=listing_id).latest("time")
        # high_bid = Bids.objects.filter(listing=lst).latest("time")
        high_bid = Bids.objects.filter(listing=lst).order_by("amount")
        high_bid = high_bid[len(high_bid)-1]

    return render(request, "auctions/listing.html", {

        "listing_data": Listing.objects.get(id=listing_id),
        "bids": new_bid,
        "high_bid": high_bid,
        "comments": new_comment,
        "comment_data": Comments.objects.filter(listing=lst),
        "seller" : Listing.objects.get(id=listing_id).seller,
        "winner" : lst.winner,
        "bid_warning": bid_warning

    })

def close_listing(request, listing_id, winner=None):

    win_user = get_object_or_404(User, username=winner)

    lst = get_object_or_404(Listing, id=listing_id)

    lst.winner = win_user

    lst.save()
    
    return redirect("listing", listing_id)

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request, category):

    # Get ID for category
    id = Category.objects.get(name=category)
    
    items = Listing.objects.filter(category=id)

    return render(request, "auctions/category.html", {
        "items": items
    })