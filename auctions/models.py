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
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name



class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    auction = models.ForeignKey('Auction', on_delete=models.PROTECT)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    auction = models.ForeignKey('Auction', on_delete=models.PROTECT)
    content = models.TextField()
    