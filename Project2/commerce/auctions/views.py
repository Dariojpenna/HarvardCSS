from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import User,Auction,Category, Comment,Bid
from .forms import AuctionForm, commentForm
from pickle import NONE


def index(request):
    auctions=Auction.objects.all()
    categories= Category.objects.all()

    return render(request, "auctions/index.html",{
        'auctions':auctions,
        'categories':categories,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        print (password)
        user = authenticate(request, username=username, password=password)
        print(user)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    if request.method =='POST':
        
        cat1=Category.objects.get(CategorieName=request.POST['category'])
        auct=Auction.objects.filter(category=cat1)
        if request.POST['category'] == 'All':
            return render(request, "auctions/index.html",{
            'auctions':Auction.objects.all(),
            'categories': Category.objects.all()
            })
    
    
    return render(request, "auctions/index.html",{
        'auctions': auct,
        'categories': Category.objects.all()
        })




def createListing (request):
    if request.method == 'GET':
        form = AuctionForm()

        return render(request, 'auctions/createListing.html',{
            'form':form,
            'categories': Category.objects.all(),

        })

    if request.method == 'POST':
        
        courrentUser=request.user
        newPrice=request.POST['bid']
        bid=Bid(bid=newPrice,user=courrentUser)
        bid.save()
        
        cat1=Category.objects.get(CategorieName=request.POST['category'])
        auction=Auction(article= request.POST['article'], price=bid, description= request.POST['description'],image=request.FILES['image'], category=cat1, owner=courrentUser )
        auction.save()
    
        auctions=Auction.objects.all
            
        messages.success(request,'your product was successfully created')
        return render (request, 'auctions/index.html',{
            'auctions':auctions,
            'categories': Category.objects.all(),
            })


def product(request,id):
    
    product=Auction.objects.get(id=id)
    productList= request.user in product.watchlist.all()
    owner = request.user.username == product.owner.username
    winner=request.user.username==product.price.user.username
    return render (request,'auctions/product.html',{
        'product':product,
        'productList':productList,
        'form':commentForm(),
        'comments':Comment.objects.filter(auction_id=id),
        'owner':owner,
        'winner':winner
    })

def addToWatchlist(request,id):
    product=Auction.objects.get(id=id)
    user= request.user
    product.watchlist.add(user)
    productList= request.user in product.watchlist.all()
    owner = request.user.username == product.owner.username
    return render (request,'auctions/product.html',{
        'product':product,
        'productList':productList,
        'form':commentForm(),
        'comments':Comment.objects.filter(auction_id=id),
        'owner':owner
    })


def removeFromWatchlist(request,id):
    product=Auction.objects.get(id=id)
    user= request.user
    product.watchlist.remove(user)
    productList= request.user in product.watchlist.all()
    owner = request.user.username == product.owner.username
    return render (request,'auctions/product.html',{
        'product':product,
        'productList':productList,
        'form':commentForm(),
        'comments':Comment.objects.filter(auction_id=id),
        'owner':owner
    })

def watchlist(request):
    user=request.user
    watchlistProduct=user.watchlist.all()
    
    return render(request,'auctions/watchlist.html',{
        'auctions': watchlistProduct,
        'categories': Category.objects.all(),
        
    })


def comment (request,id):
    user =request.user
    product = Auction.objects.get(id=id)
    form=commentForm()
    comment=Comment( name=user,auction=product,comment= request.POST ['comment'])       
        
    comment.save()
    owner = request.user.username == product.owner.username
    return render (request,'auctions/product.html',{
        'product':product,
        'productList':product,
        'form':form,
        'comments':Comment.objects.filter(auction_id=id),
        'owner':owner
    })


def offer(request,id):
    product = Auction.objects.get(id=id)
    newOffer=request.POST['offer']
    user=request.user
    auction=Auction.objects.get(id=id)
    owner = request.user.username == product.owner.username
    if request.method == 'GET':
        return render (request,'auctions/product.html',{
        'product':auction,       
        'form':commentForm(),
        'comments':Comment.objects.filter(auction_id=id),
        'owner':owner
        })
    else:
        if (int(newOffer)<auction.price.bid ):
            messages.success(request,'your offer must be higher than the current price')
            return render (request,'auctions/product.html',{
                'product':auction,
                'form':commentForm(),
                'comments':Comment.objects.filter(auction_id=id),
                'accepted': False,
                'owner':owner
            })
        else:
            newBid= Bid(user=user,bid=int(newOffer))
            newBid.save()
            auction.price= newBid
            auction.save()
            messages.success(request,'successful offer')
            return render (request,'auctions/product.html',{
                'product':auction,
                'form':commentForm(),
                'comments':Comment.objects.filter(auction_id=id),
                'accepted':True,
                'owner':owner
            })

def removeAuction(request,id):
    product=Auction.objects.get(id=id)
    product.activated=False
    product.save()
    productList= request.user in product.watchlist.all()
    owner = request.user.username == product.owner.username
    return render (request,'auctions/product.html',{
        'product':product,
        'productList':productList,
        'form':commentForm(),
        'comments':Comment.objects.filter(auction_id=id),
        
    })
            
            

def closed(request):
    auctions=Auction.objects.all()
    categories= Category.objects.all()

    return render(request, "auctions/closedListings.html",{
        'auctions':auctions,
        'categories':categories,
    })