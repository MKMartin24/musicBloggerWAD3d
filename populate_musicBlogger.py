import os
os.environ.setdefault('DJANGO_SSETTINGSMODULE','musicBloggerWAD3d.settings')

import django
django.setup
from musicBlogger.models import Songs, UserProfile, Blogs, Comments
from django.contrib.auth.models import User

def populate():
    
    madeBy = [
        {'user': 'The Weeknd'}
    ]
    blogs_title = [
        {'title': 'Top song of 2022'}
    ]
    date = [
        {'date': 23/2/2023}
    ]
    Songs_name = [
        'song_name': 'blinding lights'
    ]
    Songs = [
        {'name':Songs_name, 'text':'Best song', 'spotifyURL':'https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ', 'youtubeURL':'https://www.youtube.com/watch?v=4NRXx6U8ABQ&ab_channel=TheWeekndVEVO', 
         'description':'by The Weeknd','madeBy':madeBy}
    ]
    userProfile = [
        {'user': 'Jay345', 'text':'Normal person who love The weekend', 'likedSong':'Blindlights','artist':'Jay', 'follows':4 }
    ]

    blogs = [ 
        {'title': blogs_title,'date': date,'text': 'No.1: Blinding lights','postedBy': madeBy}
    ]

    blog_comment = [
        {'content': 'When is the new album gonna release', 'date':date, 'commentBy':'ScH'}
    ]

    tset_users = [ 
        {'id':2900000, 'user_name':'Jay345', 'email' : 'jay345@gmail.com'}
        #,{'id':3000000, 'user_name':'Issac123','email': 'issac123@gmail.com'}
        
    ]
   
        
    for user in tset_users:
        add_user(user['id'], user['user_name'], user['email'])
    
    users = User.objects.all()
    user_list = []
    for user in users:
        user_id = user.id
        userProfile = add_user_profile(user, user_id)
        user_list.append(userProfile)

    for blogs, in blogs.items():
        name = ['Title']      
        b = add_blog(name, user_list)     
        content = blog_comment.content 
        madeBy = blog_comment.commentBy
        add_blogs_comments(content,b,madeBy)

    print("Population script finished.")

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