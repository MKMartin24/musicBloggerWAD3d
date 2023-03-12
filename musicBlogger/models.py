from django.db import models
from django.contrib.auth.models import User


class Songs (models.Model):
    name = models.CharField(max_length=128, default="No-Name")
    spotifyURL = models.CharField(max_length=128)
    youtubeURL = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    coverArt = models.ImageField(upload_to='cover_images')
    genre = models.CharField(max_length=128)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    email = models.EmailField(max_length=128, null=False)
    artist = models.BooleanField()
    review = models.BooleanField()
    artsIndustry = models.BooleanField()
    likedSong = models.ManyToManyField(Songs)
    follows = models.ManyToManyField('self')
    def __str__(self):
        return self.user.username
    


class Blogs(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateField()
    image = models.ImageField(upload_to='blog_images', blank=True)
    text = models.CharField(max_length=4096)
    postedBy = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    def __str__(self):
        return self.title

class Comments(models.Model):
    content = models.CharField(max_length=1000)
    date = models.DateField()
    blog = models.ForeignKey(Blogs, on_delete = models.CASCADE)
    commentedBy = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    def __str__(self):
        return self.content
