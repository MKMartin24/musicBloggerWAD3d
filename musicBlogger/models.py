from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    madeSongs = models.ManyToManyField(Songs)
    artistName = models.CharField(max_length=128)

class Songs (models.Model):
    name = models.CharField(max_length=128, default="No-Name")
    bio = models.CharField(max_length=1000)
    spotifyURL = models.CharField(max_length=128)
    youtubeURL = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    coverArt = models.ImageField(upload_to='cover_images')
    genre = models.CharField(max_length=128)
    madeBy = models.ForeignKey(Artist, on_delete = models.CASCADE)

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    likedSong = models.ManyToManyField(Songs)
    artist = models.ManyToManyField(Artist)
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
