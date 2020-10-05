from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import AuctionForm

from .models import User, Auction, Bid, Category

def new(request):
    if request.method == "GET":
        return render(request, "auctions/new.html", {
            "form": AuctionForm()
        })
    else:
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = Auction(**form.cleaned_data)
            auction.user = request.user
            auction.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/new.html", {
                "form": form
            })
        

def watchlist(request):
    return render(request, "auctions/watchlist.html")


def show(request, title):
    return render(request, "auctions/show.html", {
        "auction": Auction.objects.get(title=title)
    })


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
    })


def category(request):
    return render(request, "category")


def categories(request):
    return render(request, "categories")


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
