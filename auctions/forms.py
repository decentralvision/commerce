from django import forms
from django.db import models
from .models import Category

class AuctionForm(forms.Form):
    title = forms.CharField(label="Title")
    price = forms.CharField(widget=forms.NumberInput, label="Price") 
    img_url = forms.CharField(label="Image Url")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    description = forms.CharField(widget=forms.Textarea, label="Description")