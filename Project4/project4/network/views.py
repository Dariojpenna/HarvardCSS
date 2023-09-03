from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from django.core.paginator import Paginator
from .models import User,Post,Followers,Like
from django.http import JsonResponse
import json




def addLike(request,postId):
    post = Post.objects.get(id=postId)
    user = User.objects.get(id = request.user.id)
    post.like += 1
    post.save()
    newLike = Like(user= user, post= post)
    newLike.save()
    total_likes = Like.objects.filter(post=post).count()

    return JsonResponse({'message': "Like Added", 'total_likes': total_likes})

def removeLike(request,postId):
    post = Post.objects.get(id=postId)
    user = User.objects.get(id = request.user.id)
    post.like -=1
    post.save()
    unlike = Like.objects.filter(user= user, post= post)
    unlike.delete()
    total_likes = Like.objects.filter(post=post).count()

    return JsonResponse({'message': "Like Removed", 'total_likes': total_likes})

def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    currentUser = request.user
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    postInPage = paginator.get_page(pageNumber)
    likes = Like.objects.all();
    whoYouLiked = []
    
    try:
        for like in likes:
            if like.user.id == currentUser.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked=[]

    return render(request, "network/index.html",{
        "currentUser":currentUser,
        "postInPage": postInPage,
        "whoYouLiked": whoYouLiked,
        "likes":likes,
        
        
    })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def newPost(request):
    return render(request, "network/newPost.html",{
       "form":PostForm,
       "user": request.user 
    })

def addPost(request):

    postInPage = None
    if(request.method == "POST"):
        currentUser = request.user
        content = request.POST["postContent"]
        post = Post(post = content, user = currentUser)
        post.save()
        posts = Post.objects.all()

        posts = Post.objects.all().order_by("id").reverse()
    
        paginator = Paginator(posts, 10)
        pageNumber = request.GET.get('page')
        postInPage = paginator.get_page(pageNumber)
    return HttpResponseRedirect(reverse(index))
    
    
def profile(request,userConected):
    
    userProfile= User.objects.get(username=userConected)
    posts = Post.objects.filter(user=userProfile).order_by("id").reverse()
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    postInPage = paginator.get_page(pageNumber)
    
    following = Followers.objects.filter(userFollowed= userProfile.id)
    followers = Followers.objects.filter(userWhoFollows = userProfile.id)
    isFollower = False
    if request.user.is_authenticated:
        isFollower = followers.filter(userFollowed=  request.user)
    
    return render(request, "network/profile.html",{
         "currentUser":request.user,
        "postInPage":postInPage,
        "userProfile": userProfile,
        "following": following, 
        "followers":followers,
        "isFollower":isFollower
    })



def follow(request):
    userf = request.POST['userFollow']
    userFollow = User.objects.get(username = userf)
    currentUser = request.user
    f = Followers(userWhoFollows=userFollow,userFollowed=currentUser)
    f.save()

    return HttpResponseRedirect(reverse(profile, kwargs={"userConected":userFollow.username}))


def unfollow(request):
    userf = request.POST['userFollow']
    userFollow = User.objects.get(username = userf)
    currentUser = request.user
    f = Followers.objects.get(userWhoFollows=userFollow,userFollowed=currentUser)
    f.delete()

    return HttpResponseRedirect(reverse(profile, kwargs={"userConected":userFollow.username}))

def following(request):
    
    followed = Followers.objects.filter(userFollowed = request.user)
    allpost= Post.objects.all().order_by("id").reverse()
    followingPost=[]

    for post in allpost:
        for person in followed:
            if person.userWhoFollows == post.user:
                followingPost.append(post)
        
        
    paginator = Paginator(followingPost, 10)
    pageNumber = request.GET.get('page')
    postInPage = paginator.get_page(pageNumber)            
                
    return render(request, "network/following.html",{
            "postInPage": postInPage,
            
    })        
    

def edit(request,postId):
    if request.method == "POST":
        data = json.loads(request.body)
        post_content_edit = data.get('postContentEdit')

        # Realiza las operaciones necesarias para guardar el contenido editado
        post = Post.objects.get(id=postId)
        post.post= post_content_edit
        post.save()
        # en tu base de datos u otro almacenamiento persistente

        # Aquí simplemente devolvemos la misma información recibida como respuesta
        response_data = {
            'message': "Successful Modification",
            'postContentEdit': post_content_edit
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

