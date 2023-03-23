from django.test import TestCase
from django.contrib.auth.models import User
from musicBlogger.models import UserProfile, Blogs, Comments
from musicBlogger.forms import UserForm, UserProfileForm, BlogForm, CommentForm

class UserFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }
        self.invalid_data = {
            'username': 'testuser#',  # username contains invalid characters which should give an error
            'email': 'testuser',  # email is invalid but it should still save
            'password': 'test',  # short password but it should still save
        }

    def test_user_form_valid_data(self):
        form = UserForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_data(self):
        form = UserForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.valid_data = {
            'text': 'This is a test user profile',
            'image': None,
        }
        self.invalid_data = {
            'text': '',  # text field is empty
            'image': 'invalid-image-data',  # invalid image data which should not be saved
        }

    def test_user_profile_form_valid_data(self):
        form = UserProfileForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_invalid_data(self):
        form = UserProfileForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_user_profile_form_save(self):
        form = UserProfileForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user_profile = form.save(commit=False)
        user_profile.user = self.user
        user_profile.save()
        self.assertIsNotNone(user_profile.pk)
        self.assertEqual(user_profile.user, self.user)
class BlogFormTest(TestCase):

    def test_valid_form(self):
        form = BlogForm(data={
            'title': 'Test Blog',
            'image': 'test.jpg',
            'text': 'This is a test blog post.'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = BlogForm(data={
            'title': '',
            'image': 'test.jpg',
            'text': 'This is a test blog post.'
        })
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):

    def test_valid_form(self):
        form = CommentForm(data={
            'content': 'This is a test comment.'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CommentForm(data={
            'content': ''
        })
        self.assertFalse(form.is_valid())
