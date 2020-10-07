from django import forms
from django.db import models
from .models import Category

class AuctionForm(forms.Form):
    title = forms.CharField(label="Title")
    price = forms.CharField(widget=forms.NumberInput, label="Price") 
    img_url = forms.CharField(label="Image Url")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    active = forms.BooleanField(widget=forms.HiddenInput, label="Active", required=False)


class WauctionForm(forms.Form):
    auction = forms.CharField(widget=forms.HiddenInput, label="Auction")
    active = forms.BooleanField(widget=forms.CheckboxInput,label="Add to Watchlist", required=False)

class BidForm(forms.Form):
    
    auction = forms.CharField(widget=forms.HiddenInput, label="Auction")
    user = forms.CharField(widget=forms.HiddenInput, label="User")
    amount = forms.CharField(widget=forms.NumberInput, label="Price")
    
    # def process(self):
    #     data = self.cleaned_data
    #     return data