import pdb
from django.db.models import Max
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AuctionForm, WauctionForm, BidForm, EndAuctionForm
from .models import User, Auction, Bid, Category, Wauction
import json


def new(request):
    if request.method == "GET":
        return render(request, "auctions/new.html", {"form": AuctionForm()})
    else:
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = Auction(**form.cleaned_data)
            auction.user = request.user
            auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new.html", {"form": form})


def close(request, title):
    auction = Auction.objects.get(title=title)
    auction.closed = True
    auction.winner_id = request.user.id
    auction.save()
    return redirect("/auction/{}".format(auction.title))


def bid(request):
    form = BidForm()
    if request.method == "POST":
        user = request.user
        form = BidForm(request.POST)
        if form.is_valid():
            auction = form.cleaned_data["auction"]
            if auction.price < float(form.cleaned_data["amount"]):
                auction.price = float(form.cleaned_data["amount"])
                auction.save()
                form.save(commit=True)
            else:
                messages.add_message(request, messages.ERROR, 'Bid amount must be greater than auction price.')
        # Bid.objects.create(
        #     amount=form.cleaned_data["amount"],

        # )

    return redirect("/auction/{}".format(auction.title))

    # bid logic
    # <!-- for MODEL form verify larger than other bids with auction id matching request auction id-->


def watchlist(request):
    # if user is logged_in
    # display user's watchlist
    user = request.user
    if user.is_authenticated:
        if request.method == "GET":
            # check if there are any wauctions
            if Wauction.objects.filter(user=user, active=True).exists():
                wauctions = Wauction.objects.get(user=user, active=True)
                if isinstance(wauctions, list):

                    def get_auctions(wauction):
                        return wauction.auction

                    auctions = wauctions.map(get_auctions, wauctions)
                else:
                    auctions = [wauctions.auction]

                return render(
                    request, "auctions/watchlist.html", {"auctions": auctions}
                )
            else:
                return render(request, "auctions/watchlist.html", {"auctions": []})
        else:
            auction_id = int(request.POST["auction"])
            auction = Auction.objects.get(pk=auction_id)
            wauction, created = Wauction.objects.get_or_create(
                user=user, auction=auction
            )
            wauction.active = not bool(wauction.active)
            wauction.save()
            return redirect("/auction/{}".format(auction.title))

    else:
        return redirect("index")


def show(request, title):
    if request.method == "GET":
        user = User.objects.get(username=request.user)
        auction = Auction.objects.get(title=title)
        # pdb.set_trace()
        # pass wuaction status
        if Wauction.objects.filter(user=user, auction=auction).exists():
            wauction = Wauction.objects.get(user=user, auction=auction)
            active = wauction.active
        else:
            active = False
        # pass bid form and data
        bid_form = BidForm({"auction": auction, "user": user, "amount": auction.price})
        end_auction = EndAuctionForm({"closed": auction.closed})
        return render(
            request,
            "auctions/show.html",
            {
                "auction": auction,
                "wauction_form": WauctionForm({"auction": auction.id, "active": active}),
                "bid_form": bid_form,
                "end_auction": end_auction
            }
        )
    else:
        return redirect('index')
        # return something


def index(request):
    return render(request, "auctions/index.html", {"auctions": Auction.objects.all()})


def category(request, name):
    auctions = Auction.objects.filter(category=name)
    # get objects with category matching name
    return render(request, "auctions/categories.html", {"auctions": auctions})


def categories(request):
    category_list = Category.objects.all()
    # get list of category names
    return render(request, "auctions/categories.html", {"category_list": category_list})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
