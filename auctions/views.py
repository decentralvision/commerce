import pdb
from django.db.models import Max
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AuctionForm, WauctionForm, BidForm, EndAuctionForm, CommentForm
from .models import User, Auction, Bid, Category, Wauction, Comment
import json


def show(request, id):
    user = request.user
    auction = Auction.objects.get(id=id)
    comments = Comment.objects.filter(auction=auction)
    highest_bidder = get_highest_bidder(auction)
    number_of_bids = get_number_of_bids(auction)
    if user.is_authenticated:
        user = User.objects.get(username=user)
        # make forms
        if Wauction.objects.filter(user=user, auction=auction).exists():
            wauction = Wauction.objects.get(user=user, auction=auction)
            active = wauction.active
        else:
            wauction = Wauction(user=user, auction=auction)
            active = False
        wauction_obj = {"auction": auction.id, "active": active}
        bid_form = BidForm({"auction": auction, "user": user, "amount": auction.price})
        end_auction_form = EndAuctionForm({"closed": auction.closed})
        comment_form = CommentForm({"auction": auction, "user": user})
        # create comment form and pass
        return render(
            request,
            "auctions/show.html",
            {
                "auction": auction,
                "wauction_form": WauctionForm(wauction_obj),
                "bid_form": bid_form,
                "end_auction": end_auction_form,
                "comment_form": comment_form,
                "comments": comments,
                "number_of_bids": number_of_bids,
                "highest_bidder": highest_bidder,
                "is_current_user_winner": user == auction.winner,
                "is_current_user_owner": user == auction.user
            }
        )
    else:
        return render(
            request,
            "auctions/show.html",
            {
                "auction": auction,
                "wauction_form": WauctionForm(),
                "bid_form": BidForm(),
                "end_auction": EndAuctionForm(),
                "comments": comments,
                "number_of_bids": number_of_bids,
                "highest bidder": highest_bidder,
                "is_current_user_winner": False,
                "is_current_user_owner": False
            }
        )


def index(request):
    return render(request, "auctions/index.html", {"auctions": Auction.objects.filter(closed=False)})


def category(request, name):
    auctions = Auction.objects.filter(category__name=name, closed=False)
    return render(request, "auctions/category.html", {"name": name, "auctions": auctions})


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

@login_required(login_url='login')
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

@login_required(login_url='login')
def comment(request):
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                auction = form.cleaned_data["auction"]
                # check if it's a duplicate and that it has some content
                if form.cleaned_data["content"]:
                    if not Comment.objects.filter(user=user, content=form.cleaned_data["content"], auction=form.cleaned_data["auction"]):
                        form.save(commit=True)
                    else:
                        messages.add_message(request, messages.ERROR, 'This comment is a duplicate.')
                else:
                    messages.add_message(request, messages.ERROR, 'Comment must not be empty.')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
def close(request, id):
    auction = Auction.objects.get(id=id)
    auction.closed = True
    if get_highest_bidder(auction)["username"] == "No bids yet":
        auction.winner = request.user
    else:
        auction.winner = get_highest_bidder(auction)
    auction.save()
    return redirect("/auction/{}".format(id))

@login_required(login_url='login')
def bid(request):
    form = BidForm()
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            auction = form.cleaned_data["auction"]
            if auction.price < float(form.cleaned_data["amount"]):
                auction.price = float(form.cleaned_data["amount"])
                auction.save()
                form.save(commit=True)
            else:
                messages.add_message(request, messages.ERROR, 'Bid amount must be greater than auction price.')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
def watchlist(request):
    # if user is logged_in
    # display user's watchlist
    user = request.user
    if user.is_authenticated:
        if request.method == "GET":
            # check if there are any wauctions
            if Wauction.objects.filter(user=user, active=True).exists():
                wauctions = Wauction.objects.filter(user=user, active=True)
                # get watched auction items where user=user and active=true
                if wauctions.count() > 1:
                    # get auction items from watched auction items
                    return render(request, "auctions/watchlist.html", {"auctions": wauctions})
                    # auctions = wauctions.auction
                    # return render(request, "auctions/watchlist.html", {"auctions": auctions})
                else:
                    auction = wauctions[0].auction
                    return render(request, "auctions/watchlist.html", {"auction": auction})
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
            return redirect("/auction/{}".format(auction.id))

    else:
        return redirect("index")


# extract these into the model
def get_highest_bidder(auction):
    if Bid.objects.filter(auction=auction, amount=auction.price):
        winning_bid = Bid.objects.get(auction=auction, amount=auction.price)
    else:
        # probably a better way of doing this
        return {"username": "No bids yet"}
    return winning_bid.user

def get_number_of_bids(auction):
    number_of_bids = Bid.objects.filter(auction=auction).count()
    if number_of_bids:
        return number_of_bids
    else:
        return 0
    