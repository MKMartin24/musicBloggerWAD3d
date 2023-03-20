import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicBloggerWAD3d.settings')

import django
django.setup()
from musicBlogger.models import *
from django.contrib.auth.models import User
from django.utils import timezone


def populate():

    test_users = [
        {'name': 'Jay345', 'email': 'jay345@gmail.com', 'password': 'Jay345123'},
        {'name': 'Issac123', 'email': 'issac123@gmail.com', 'password': 'Issac123456'},
        {'name': 'Henry678', 'email': 'henry678@gmail.com', 'password': 'henry6789'},
    ]

    for i in test_users:
        add_user(i['name'], i['password'], i['email'])

    userprofile_list = [
        {'name': User.objects.get(username='Jay345'), 'text': 'Normal person who love The weekend',
         'image_name': 'userProfile1.jpg'},
        {'name': User.objects.get(username='Issac123'), 'text': 'No.1 fans of The weekend',
         'image_name': 'userProfile1.jpg'},
        {'name': User.objects.get(username='Henry678'), 'text': 'The weekend is the best',
         'image_name': 'userProfile1.jpg'},
    ]

    for i in userprofile_list:
        add_user_profile(i['name'], i['text'], i['image_name'])

    blogs_list = [
        {'name': 'My favourite music in 2021', 'image': 'blogs1.jpg', 'text': 'No.1: Blinding light', 'post_by': UserProfile.objects.get(text='Normal person who love The weekend')},
        {'name': 'My favourite music all the time', 'image': 'blogs2.jpg', 'text': "No.1: It's my life", 'post_by': UserProfile.objects.get(text='The weekend is the best')}
    ]

    for i in blogs_list:
        add_blog(i['name'], i['image'], i['text'], i['post_by'])

    comments_list = [
        {'content': 'When is the new album gonna release', 'blog': Blogs.objects.get(name='My favourite music in 2021'),
         'commentBy': UserProfile.objects.get(name=User.objects.get(username='Jay345'))}
    ]

    for i in comments_list:
        add_comment(i['content'], i['blog'], i['commentBy'])

    artist_list = [
        {'artistName': 'The weeknd'},
        {'artistName': 'Linkin Park'},
        {'artistName': 'Coldplay'}

    ]

    for i in artist_list:
        add_artist(i['artistName'])

    songs_list = [
        {'name': 'Paradise', 'text': 'Gold', 'spotifyURL': "https://open.spotify.com/search/Coldplay%20Para",
         'youtubeURL': "https://www.youtube.com/watch?v=1G4isv_Fylg&ab_channel=Coldplay",
         'description': '11 years ago, but still gold', 'image': 'song1.jpg', 'genre': 'pop music',
         'madeBy': Artist.objects.get(artistName='Coldplay')}
    ]

    for i in songs_list:
        add_song(i['name'], i['text'], i['spotifyURL'], i['youtubeURL'], i['description'], i['image'], i['genre'], i['madeBy'])

    a = UserProfile.objects.get(text='Normal person who love The weekend')
    b = UserProfile.objects.get(text='No.1 fans of The weekend')
    c = UserProfile.objects.get(text='The weekend is the best')

    s = Songs.objects.get(name='Paradise')
    # s2 = Songs.objects.get(name='')
    a.likedSong.add(s)
    # a.likedSong.add(s, s2, s3)

    art1 = Artist.objects.get(artistName='Coldplay')
    art2 = Artist.objects.get(artistName='The weeknd')
    art3 = Artist.objects.get(artistName='Linkin Park')
    a.artist.add(art1, art2, art3)

    a.follows.add(b)
    b.follows.add(a)
    c.follows.add(a, b)

    a.save()
    b.save()
    c.save()






def add_user_profile(name, text, image_name):
    u = UserProfile.objects.get_or_create(name=name, text=text, image="/profile_images/"+image_name)[0]
    u.save()
    return u



def add_user(name, password, email):
    u = User.objects.get_or_create(username=name, email=email, last_login = timezone.now())[0]
    u.set_password(password)
    u.save()
    return u


def add_blog(name, image_name, text, postBy):
    b = Blogs.objects.get_or_create(name=name, image='/blog_images/'+image_name, text=text, postedBy=postBy)[0]
    b.save()
    return b


def add_song(name, text, spotifyURL, youtubeURL, description, image, genre, madeBy):
    s = Songs.objects.get_or_create(name=name, text=text, spotifyURL=spotifyURL, youtubeURL=youtubeURL,
                                    description=description, image="/cover_images/"+image, genre=genre, madeBy=madeBy)[0]
    s.save()
    return s

def add_comment(content, blog, commentedBy):
    com = Comments.objects.get_or_create(content = content, blog=blog, commentedBy=commentedBy)[0]
    com.save()
    return com

def add_artist(artistName):
    a = Artist.objects.get_or_create(artistName=artistName)[0]
    a.save()
    return a

# Start excution here
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
    print('Finished')