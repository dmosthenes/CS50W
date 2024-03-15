from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm

from .models import User, Listing, Bids, Comments

from datetime import datetime


class new_listing(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','imageURL','duration']

class new_bid(ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']

class new_comment(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']


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
    pass

def create_listing(request):
    if request.method == "POST":

        # Put form content into database
        form = new_listing(request.POST)
        if form.is_valid():

            user = request.user

            instance = form.save(commit=False)
            instance.seller = user

            instance.start = datetime.now()

            instance.save()




        id = instance.id
        print(id)
        
        return redirect('listing', id)

    else:

        return render(request, "auctions/create_listing.html", {
            "form": new_listing
        
        })

def listing(request, name):

    print(name)
    
    if request.method == "POST":

        pass


    else:

        return render(request, "auctions/listing.html", {

            # "listing_data": Listing.objects.get(id=listing_id),
            # "bids": new_bid,
            # # "bid_data": Bids.objects.get(id=listing_id),
            # "comments": new_comment,
            # "comment_data": Comments.objects.get(id=listing_id)

        })