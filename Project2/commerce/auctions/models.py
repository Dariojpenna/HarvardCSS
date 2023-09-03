from django.contrib.auth.models import AbstractUser
from django.db import models
from pickle import TRUE


class User(AbstractUser):
    pass


class Category(models.Model):
    CategorieName=models.CharField(max_length=64)

    def __str__(self):
        return f'{self.CategorieName}'


class Bid (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userBid')
    bid=models.IntegerField(blank=True,null=TRUE)

    def __str__(self):
        return f'{self.bid}'



class Auction(models.Model):
    
    article=models.CharField(max_length=64)
    price=models.ForeignKey(Bid,on_delete=models.CASCADE,null=True,blank=True,related_name='Bid')
    description=models.TextField(max_length=500)
    image=models.ImageField (upload_to='media', null=TRUE)
    date=models.DateField(auto_now=True,null=TRUE,blank=True)
    category=models.ForeignKey(Category , on_delete=models.CASCADE, blank=True,null=True,related_name='category')
    watchlist=models.ManyToManyField(User,blank=TRUE,null=TRUE,related_name='watchlist')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,blank=TRUE,null=TRUE,related_name='user')
    activated=models.BooleanField(default=True)
   
    def __str__(self):
        return f"{self.id}: {self.article}  {self.image} {self.price} {self.date} {self.owner} {self.activated}"


class Comment(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE,blank=TRUE,null=TRUE,related_name='userComment')
    auction=models.ForeignKey(Auction,on_delete=models.CASCADE,blank=TRUE,null=TRUE,related_name='auctionComment')
    comment=models.TextField()

    def __str__(self):
        return f"{self.name}: {self.auction}   {self.comment}"


