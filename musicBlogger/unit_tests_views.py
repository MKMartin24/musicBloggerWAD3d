from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from musicBlogger.models import *
from musicBlogger.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            text='user profile text'
        )
        self.blog = Blogs.objects.create(
            title='test blog',
            date='2002-10-01',
            text='test blog',
            postedBy=self.user_profile
        )
        self.comment = Comments.objects.create(
            content='test comment',
            date='2002-10-10',
            blog=self.blog,
            commentedBy=self.user_profile
        )


    def test_index_view(self):
        response = self.client.get(reverse('musicBlogger:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/index.html')

    def test_about_view(self):
        response = self.client.get(reverse('musicBlogger:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/about.html')

    def test_user_login_view(self):
        response = self.client.get(reverse('musicBlogger:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/login.html')
        #Testing with valid password
        response = self.client.post(reverse('musicBlogger:login'), {'username': 'user', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # successful redirect
        self.assertRedirects(response, reverse('musicBlogger:index'))
        #Testing with invalid password
        response = self.client.post(reverse('musicBlogger:login'), {'username': 'user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)  # failed login, still on the same page
        self.assertContains(response, 'Invalid login details supplied.')
        #Testing with invalid account name
        response = self.client.post(reverse('musicBlogger:login'), {'username': 'wrong_user', 'password': 'password'})
        self.assertEqual(response.status_code, 200)  # failed login, still on the same page
        self.assertContains(response, 'Invalid login details supplied.')

    def test_user_logout_view(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('musicBlogger:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('musicBlogger:index'))

    def test_search_blogs_view(self):
        response = self.client.get(reverse('musicBlogger:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/search.html')

    def test_contact_us_view(self):
        response = self.client.get(reverse('musicBlogger:contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/contact_us.html')

    def test_new_account_view(self):
        response = self.client.get(reverse('musicBlogger:new_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/new_account.html')
        #Testing valid form submission
        response = self.client.post(reverse('musicBlogger:new_account'), {'username': 'new_user1', 'password': 'new_password','email': 'test@email.com','text': 'test text'})
        response = self.client.post(reverse('musicBlogger:login'), {'username': 'new_user1', 'password': 'new_password'})
        self.assertEqual(response.status_code, 302)  # successful redirect which indicates new account successfully created
        self.assertRedirects(response, reverse('musicBlogger:index'))
        #Testing invalid form submission
        response = self.client.post(reverse('musicBlogger:new_account'), {'username': 'new_user2', 'text': 'test text'})
        self.assertEqual(response.status_code, 200)  # invalid form submission and prints out the error dict(missing required fields)

    def test_profile_view(self):
        response = self.client.get(reverse('musicBlogger:profile', kwargs={'username': self.user_profile.user}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/profile.html')
        self.assertContains(response, self.user_profile.user) #Checks if the response contains the user's profile name or not

    def test_blog_view(self):
        response = self.client.get(reverse('musicBlogger:blog',args=[self.blog.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/viewBlog.html')
        self.assertContains(response, self.blog.title)

    def test_write_blog_view_logged_in(self):
        test_blog = {'title': 'hello','img':'blogs1.jpg', 'text': 'Test text', 'postedBy': self.user_profile}
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('musicBlogger:write_blog')) #test if we can get to write blog page after logging in
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'musicBlogger/writeBlog.html')
        response = self.client.post(reverse('musicBlogger:write_blog'),test_blog)
        self.assertEqual(response.status_code,302)
        #Check to see if we the blog has been successfully created with dynamic url
        blog = Blogs.objects.get(slug='hello')
        self.assertEqual(blog.title, 'hello')
        response = self.client.get(reverse('musicBlogger:blog', args=[blog.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hello')

    def test_add_comment_view(self):
        self.client.login(username='user', password='password') #login to comment
        test_comment = {'content': 'testing comments'}
        response = self.client.post(reverse('musicBlogger:add_comment',kwargs={'slug': 'test-blog'}), test_comment)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.blog.comments.count(), 2) #Check if the total number of comments is 2 or not



