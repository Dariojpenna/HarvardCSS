from django.contrib import admin
from .models import Category,User,Auction,Comment,Bid

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Bid)

# Register your models here.
