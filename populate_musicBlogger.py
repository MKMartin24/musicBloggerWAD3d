import os
os.environ.setdefault('DJANGO_SSETTINGSMODULE','musicBloggerWAD3d.settings')

import django
django.setup
from musicBlogger.models import UserProfile, Comments, Songs
from django.contrib.auth.models import User

def populate():
<<<<<<< Updated upstream
    
    #python_pages = [
    #]

    #django_pages = [
    #]

    #other_pages = [
    #]

    #cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            #'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            #'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}
            #}

=======
    like_Songs = [ 
        {'spotifyURL' : 'https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U', 'youtubeURL': 'https://www.youtube.com/', 'description': 'Best jazz song',
        'genre': 'jazz'}
    ]
>>>>>>> Stashed changes
    
    user = [ { 'id':1234567, 'user_name':'Issac123', 'email' : 'issac123@gmail.com'
    },
    { 'id':2900000, 'user_name':'Jay123', 'email' : 'jay123@gmail.com'
    },
    { 'id':3099999, 'user_name':'Henry123', 'email' : 'Henry123@gmail.com'
    }

    ]
    userProfile = [
        {'user': 'Issac123', 'email': 'issac123@gmail.com', 'artist': 'The weeknd', 'artIndustry': 'pop music','likedSong': 4,'artistSong': 'blinding lights'
        
        }

    ]

    blogs = [ 
        {'title': 'Top song of 2022','date': 23/2/2023,'text': 'No.1: Shape Of You','postedBy': 'Jay'
        
        }

    ]

    blog_comment = [
        {'content': 'When is the new album gonna release', 'date': 23/2/2023,'blog': 'New songs coming up','commentedBy':'Issac123'
        
        }

    ]

    #following = [ {
        
    #}
        
    #]

def add_user_profile(user, user_id):
    u = UserProfile.objects.get_or_create(user=user, user_id=user_id)[0]
    u.save()
    return u

def add_blogs_comments(post, content, user):
    com = Comments.objects.get_or_create(post=post, content=content, user=user)[0]
    com.save()
    return com



def add_user(user_id, user_name, superuser, email, first_name, last_name):
    u = User.objects.get_or_create(id=user_id, username=user_name, is_superuser=superuser, email=email,
                                   first_name=first_name, last_name=last_name)
    return u

def add_blog(name):
    Blogs = Blogs.objects.get_or_create(name=name)[0]
    Blogs.save()
    return Blogs


# Start excution here
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()