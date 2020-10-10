from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# might not be needed
from django.conf import settings


class User(AbstractUser):
    """class for user objects (users)"""


class Auction(models.Model):
    """class for managing auctions"""
    # auction data
    title = models.CharField(max_length=200)
    description = models.TextField()
    img_url = models.TextField()
    price = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    closed = models.BooleanField('Closed', default=False)
    # foreign keys
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    winner = models.ForeignKey('User', on_delete=models.PROTECT, null=True, related_name="auction_winner")

    def __str__(self):
        return self.title


class Category(models.Model):
    """class for an auction's category"""
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Bid(models.Model):
    """class for bid records"""
    amount = models.IntegerField('Amount', default=0)
    # foreign keys
    auction = models.ForeignKey('Auction', on_delete=models.PROTECT)
    user = models.ForeignKey('User', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user} in {self.auction} bid amount {self.amount}"


class Wauction(models.Model):
    """class for recording user's watched auctions and history"""
    active = models.BooleanField('Active', null=True)
    # foreign keys
    auction = models.ForeignKey('Auction', on_delete=models.PROTECT)
    user = models.ForeignKey('User', on_delete=models.PROTECT)



class Comment(models.Model):
    """class for auction comment"""
    content = models.TextField('Content', blank=True)
    # foreign keys
    auction = models.ForeignKey('Auction', on_delete=models.PROTECT)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    def __str__(self):
        return str(f"comment id: {self.id} on auction: {self.auction.title} by user: {self.user.username}")