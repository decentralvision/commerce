from django import forms
from django.db import models
from .models import Category

class AuctionForm(forms.Form):
    CATEGORIES = Category.objects.all()
    title = forms.CharField(label="Title")
    price = forms.CharField(widget=forms.NumberInput, label="Price") 
    image_url = forms.CharField(label="Image Url")
    category = forms.ChoiceField(choices=CATEGORIES)
    category = forms.CharField(label="Category")
    description = forms.CharField(widget=forms.Textarea, label="Description")

    

