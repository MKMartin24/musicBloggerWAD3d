from django.db import models
from django.contrib.auth.models import User


class Songs (models.Model):
    spotifyURL = models.CharField(128)
    youtubeURL = models.CharField(128)
    description = models.CharField(512)
    coverArt = models.ImageField(upload_to='cover_images')
    genre = models.CharField(128)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(30, unique=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    artist = models.BooleanField()
    review = models.BooleanField()
    artsIndusry = models.BooleanField()
    likedSong = models.ManyToManyField(Songs)
    artistSong = models.ManyToManyField(Songs)
    follows = models.ManyToManyField('self', symmetrical=False)
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
    title = models.CharField(128)
    date = models.DateField()
    image = models.ImageField(upload_to='blog_images')
    text = models.CharField(4096)
    postedBy = models.ManyToManyField(UserProfile)
    def __str__(self):
        return self.title

class Comments(models.Model):
    content = models.CharField(1000)
    date = models.DateField()
    blog = models.ForeignKey(Blogs)
    commentedBy = models.ManyToManyField(UserProfile)
    def __str__(self):
        return self.content
