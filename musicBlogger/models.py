from django.db import models
from django.contrib.auth.models import User


class Songs (models.Model):
    spotifyURL = models.CharField(max_length=128)
    youtubeURL = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    coverArt = models.ImageField(upload_to='cover_images')
    genre = models.CharField(max_length=128)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=30, unique=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    artist = models.BooleanField()
    review = models.BooleanField()
    artsIndusry = models.BooleanField()
    likedSong = models.ManyToManyField(Songs)
    follows = models.ManyToManyField('self')
    def __str__(self):
        return self.user.username
    

# class UserRelationship(models.Model):
#     types = models.ManyToManyField('RelationshipType', blank=True,
#                                    related_name='user_relationships')
#     from_contact = models.ForeignKey('User', related_name='from_user')
#     to_contact = models.ForeignKey('User', related_name='to_user')
#     class Meta:
#         unique_together = ('from_user', 'to_user')


class Blogs(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateField()
    image = models.ImageField(upload_to='blog_images')
    text = models.CharField(max_length=4096)
    postedBy = models.ManyToManyField(UserProfile)
    def __str__(self):
        return self.title

class Comments(models.Model):
    content = models.CharField(max_length=1000)
    date = models.DateField()
    blog = models.ForeignKey(Blogs, on_delete = models.CASCADE)
    commentedBy = models.ManyToManyField(UserProfile)
    def __str__(self):
        return self.content
