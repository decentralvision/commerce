from django import forms
from django.db import models
from .models import Category, Bid, Auction


class AuctionForm(forms.Form):
    title = forms.CharField(label="Title")
    price = forms.CharField(widget=forms.NumberInput, label="Price")
    img_url = forms.CharField(label="Image Url")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    closed = forms.BooleanField(
        widget=forms.CheckboxInput(), label="End Auction", required=False
    )


class WauctionForm(forms.Form):
    auction = forms.CharField(widget=forms.HiddenInput, label="Auction")
    active = forms.BooleanField(
        widget=forms.CheckboxInput(), label="Add to Watchlist", required=False
    )


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["user", "auction", "amount"]
        widgets = {"auction": forms.HiddenInput(), "user": forms.HiddenInput()}

class EndAuctionForm(AuctionForm):
    class Meta:
        model = Auction
        fields = ["closed"]
        widgets = {"closed": forms.CheckboxInput()}