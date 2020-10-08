from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    pass


class Auction(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    img_url = models.TextField()
    price = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    closed = models.BooleanField('Closed', default=False)
    winner = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name="auction_winner")

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    auction = models.ForeignKey('Auction', on_delete=models.PROTECT)
    amount = models.IntegerField('Amount', default=0)

    def __str__(self):
        return f"{self.user} in {self.auction} bid amount {self.amount}"

class Wauction(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    auction = models.ForeignKey('Auction', on_delete=models.PROTECT)
    active = models.BooleanField('Active', null=True)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, null=True)
    auction = models.ForeignKey('Auction', on_delete=models.PROTECT, null=True)
    content = models.TextField()
