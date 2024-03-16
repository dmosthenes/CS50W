from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing')

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    imageURL = models.CharField(max_length=200, blank=True)
    start = models.TimeField()
    duration = models.DurationField()
    category = models.OneToOneField('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, by {self.seller}, from {self.start}, with id: {self.id}"

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.IntegerField()
    time = models.TimeField()

class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=240)
    time = models.TimeField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=100)