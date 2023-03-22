import os
import warnings
import importlib
import datetime
from .models import Artist, Songs, UserProfile, Blogs, Comments
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}MODELS TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class DatabaseConfigurationTests(TestCase):
 
    def setUp(self):
        pass
    
    def does_gitignore_include_database(self, path):
        """
        Takes the path to a .gitignore file, and checks to see whether the db.sqlite3 database is present in that file.
        """
        f = open(path, 'r')
        
        for line in f:
            line = line.strip()
            
            if line.startswith('db.sqlite3'):
                return True
        
        f.close()
        return False
    
    def test_databases_variable_exists(self):
        """
        Does the DATABASES settings variable exist, and does it have a default configuration?
        """
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable, which is required. {FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable. Check the start of Chapter 5.{FAILURE_FOOTER}")
    
    def test_gitignore_for_database(self):
        """
        If you are using a Git repository and have set up a .gitignore, checks to see whether the database is present in that file.
        """
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()
        
        if git_base_dir.startswith('fatal'):
            warnings.warn("You don't appear to be using a Git repository for your codebase. Although not strictly required, it's *highly recommended*. Skipping this test.")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')
            
            if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path), f"{FAILURE_HEADER}Your .gitignore file does not include 'db.sqlite3' -- you should exclude the database binary file from all commits to your Git repository.{FAILURE_FOOTER}")
            else:
                warnings.warn("You don't appear to have a .gitignore file in place in your repository. We ask that you consider this! Read the Don't git push your Database paragraph in Chapter 5.")


class Chapter5ModelTests(TestCase):
    """
    Are the models set up correctly, and do all the required attributes (post exercises) exist?
    """
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='user1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='user2'
        )
        self.artist = Artist.objects.create(artistName='artist')
        self.song = Songs.objects.create(
            name='song',
            text='song text',
            spotifyURL='https://spotify.com/test',
            youtubeURL='https://youtube.com/test',
            description='song description',
            image='sing/image.png',
            genre='song genre',
            madeBy=self.artist
        )
        self.user_profile1 = UserProfile.objects.create(
            name=self.user1,
            text='user1 profile text'
        )
        self.user_profile2 = UserProfile.objects.create(
            name=self.user2,
            text='user1 profile text'
        )
        self.user_profile1.likedSong.add(self.song)
        self.user_profile1.follows = [self.user2.id]
        self.blog = Blogs.objects.create(
            name='blog',
            date='2002-10-01',
            text='blog text',
            postedBy=self.user_profile1
        )
        self.comment = Comments.objects.create(
            content='comment content',
            date='2002-10-10',
            blog=self.blog,
            commentedBy=self.user_profile1
        )
    
    def test_artist_creation(self):
        artist = Artist.objects.get(artistName='artist')
        self.assertEqual(artist.artistName, 'artist')

    def test_song_creation(self):
        song = Songs.objects.get(name='song')
        self.assertEqual(song.name, 'song')
        self.assertEqual(song.text, 'song text')
        self.assertEqual(song.spotifyURL, 'https://spotify.com/test')
        self.assertEqual(song.youtubeURL, 'https://youtube.com/test')
        self.assertEqual(song.description, 'song description')
        self.assertEqual(song.image, 'song/image.png')
        self.assertEqual(song.genre, 'song genre')
        self.assertEqual(song.madeBy, self.artist)

    def test_user_profile_creation(self):
        user_profile = UserProfile.objects.get(name=self.user)
        self.assertEqual(user_profile.name, self.user)
        self.assertEqual(user_profile.text, 'user1 profile text')
        self.assertEqual(len(user_profile.follows), 1)
        self.assertEqual(user_profile.likedSong.all()[0], self.song)

    def test_blog_creation(self):
        blog = Blogs.objects.get(name='blog')
        self.assertEqual(blog.title, 'blog')
        self.assertEqual(blog.date, '2022-01-01')
        self.assertEqual(blog.text, 'blog text')
        self.assertEqual(blog.postedBy, self.user_profile1)

    def test_comment_creation(self):
        comment_date_str = datetime.date(2002, 10, 10).strftime('%Y-%m-%d')
        comment = Comments.objects.get(content='comment content')
        self.assertEqual(comment.content, 'comment content')
        self.assertEqual(comment.date, comment_date_str)
        self.assertEqual(comment.blog, self.blog)
        self.assertEqual(comment.commentedBy, self.user_profile1)
