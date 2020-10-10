from django import forms
from django.db import models
from .models import Category, Bid, Auction, Comment


class CommentForm(forms.ModelForm):
    """create comment form"""
    class Meta:
        model = Comment
        fields = ["user", "auction", "content"]
        widgets = {
            "user":forms.HiddenInput(), 
            "auction": forms.HiddenInput(), 
            "content": forms.Textarea()
            }


class AuctionForm(forms.Form):
    """create auction form"""
    title = forms.CharField(label="Title")
    price = forms.CharField(widget=forms.NumberInput, label="Price")
    img_url = forms.CharField(label="Image Url", required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    closed = forms.BooleanField(
        widget=forms.CheckboxInput(), label="End Auction", required=False
    )


class WauctionForm(forms.Form):
    """create or remove auction from watchlist form"""
    auction = forms.CharField(widget=forms.HiddenInput, label="Auction")
    active = forms.BooleanField(
        widget=forms.CheckboxInput(), label="Add to Watchlist", required=False
    )


class BidForm(forms.ModelForm):
    """create bid record form"""
    class Meta:
        model = Bid
        fields = ["user", "auction", "amount"]
        widgets = {"auction": forms.HiddenInput(), "user": forms.HiddenInput()}

class EndAuctionForm(AuctionForm):
    """end auction form (set closed to True)"""
    class Meta:
        model = Auction
        fields = ["closed"]
        widgets = {"closed": forms.CheckboxInput()}