from django.forms import ModelForm
from .models import Auction,Comment

class AuctionForm (ModelForm):
    class Meta:
        model= Auction
        exclude = ('date','owner', 'watchlist','price',)

class commentForm (ModelForm):
    class Meta:
        model = Comment
        exclude = ('auction', 'name')