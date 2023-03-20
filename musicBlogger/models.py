from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Artist(models.Model):
    artistName = models.CharField(max_length=128)
    def __str__(self):
        return self.artistName

class Songs (models.Model):
    name = models.CharField(max_length=128, default="No-Name")
    text = models.CharField(max_length=1000)
    spotifyURL = models.CharField(max_length=128)
    youtubeURL = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    image = models.ImageField(upload_to='cover_images')
    genre = models.CharField(max_length=128)
    madeBy = models.ForeignKey(Artist, on_delete = models.CASCADE)
    def __str__(self):
        return self.name

    
class UserProfile(models.Model):
    name = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='profile_images', blank=True)
    likedSong = models.ManyToManyField(Songs, related_name='liked_song')
    artist = models.ManyToManyField(Artist)
    follows = models.ManyToManyField('self')

    # list of follows_user's id
    # [2, 3, 4]
    # follows = models.JsonField()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.username)
        super(UserProfile, self).save(*args, **kwargs)
    def __str__(self):
        return self.name.username


class Blogs(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images', blank=True)
    text = models.CharField(max_length=4096)
    postedBy = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    def __str__(self):
        return self.name


class Comments(models.Model):
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blogs, on_delete = models.CASCADE)
    commentedBy = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    def __str__(self):
        return self.content