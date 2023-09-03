from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    def __str__(self):
        return f"{self.profile_image.url if self.profile_image else 'No image'}"


class Post(models.Model):
    post = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userPost')
    like = models.IntegerField(default=0,  validators=[MinValueValidator(0)])
    def __str__(self):
        return f"{self.user}: {self.post}   {self.date}"
    
class Followers(models.Model):
    userFollowed = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userFollowed');
    userWhoFollows = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userWhoFollows');
    def __str__(self):
        return f"{self.userFollowed}: {self.userWhoFollows}"
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userLike');
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,null=False,related_name='postLike');
    def __str__(self):
        return f"{self.user}: {self.post}"
