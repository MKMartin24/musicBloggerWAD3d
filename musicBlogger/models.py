from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Artist(models.Model):
    artistName = models.CharField(max_length=128)

    def __str__(self):
        return self.artistName


class Songs(models.Model):
    name = models.CharField(max_length=128, default="No-Name")
    text = models.CharField(max_length=1000)
    spotifyURL = models.CharField(max_length=128)
    youtubeURL = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    image = models.ImageField(upload_to='cover_images')
    genre = models.CharField(max_length=128)
    madeBy = models.ForeignKey(Artist, related_name='songs', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Songs"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    text = models.CharField(max_length=1000,default='')
    image = models.ImageField(upload_to='profile_images', blank=True)
    likedSong = models.ManyToManyField(Songs, related_name='user_profile')
    artist = models.ManyToManyField(Artist, related_name='user_profile')
    # list of follows_user's id
    # [2, 3, 4]
    follows = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username




class Blogs(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images', blank=True)
    text = models.CharField(max_length=4096, default='')
    postedBy = models.ForeignKey(UserProfile, related_name='blogs', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blogs, self).save(*args, **kwargs)


class Comments(models.Model):
    content = models.CharField(max_length=1000,default='')
    date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blogs, related_name='comments', on_delete=models.CASCADE)
    commentedBy = models.ForeignKey(UserProfile, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.content