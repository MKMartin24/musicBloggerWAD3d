import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicBloggerWAD3d.settings')

import django
django.setup()
from musicBlogger.models import *
from django.contrib.auth.models import User


def populate():

    test_users = [
        {'user_name': 'Jay345', 'email': 'jay345@gmail.com', 'password': 'Jay345123'},
        {'user_name': 'Issac123', 'email': 'issac123@gmail.com', 'password': 'Issac123456'},
        {'user_name': 'Henry678', 'email': 'henry678@gmail.com', 'password': 'henry6789'},
    ]

    for i in test_users:
        add_user(i['user_name'], i['password'], i['email'])

    userprofile_list = [
        {'user': User.objects.get(username='Jay345'), 'text': 'Normal person who love The weekend',
         'image_name': 'userProfile1.jpg'},
        {'user': User.objects.get(username='Issac123'), 'text': 'No.1 fans of The weekend',
         'image_name': 'userProfile1.jpg'},
        {'user': User.objects.get(username='Henry678'), 'text': 'The weekend is the best',
         'image_name': 'userProfile1.jpg'},
    ]

    for i in userprofile_list:
        add_user_profile(i['user'], i['text'], i['image_name'])

    blogs_list = [
        {'title': 'My favourite music in 2021', 'image': 'blogs1.jpg', 'text': 'No.1: Blinding light', 'post_by': UserProfile.objects.get(text='Normal person who love The weekend')},
        {'title': 'My favourite music all the time', 'image': 'blogs2.jpg', 'text': "No.1: It's my life", 'post_by': UserProfile.objects.get(text='The weekend is the best')}
    ]

    for i in blogs_list:
        add_blog(i['title'], i['image'], i['text'], i['post_by'])

    comments_list = [
        {'content': 'When is the new album gonna release', 'blog': Blogs.objects.get(title='My favourite music in 2021'),
         'commentBy': UserProfile.objects.get(user=User.objects.get(username='Jay345'))}
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






def add_user_profile(user, text, image_name):
    u = UserProfile.objects.get_or_create(user=user, text=text, image="/profile_images/"+image_name)[0]
    u.save()
    return u


def add_user(user_name, password, email):
    u = User.objects.get_or_create(username=user_name, email=email)[0]
    u.set_password = password
    u.save()
    return u


def add_blog(title, image_name, text, postBy):
    b = Blogs.objects.get_or_create(title=title, image='/blog_images/'+image_name, text=text, postedBy=postBy)[0]
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