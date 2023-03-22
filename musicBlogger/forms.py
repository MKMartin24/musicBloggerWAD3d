from django import forms
from django.contrib.auth.models import User
from musicBlogger.models import UserProfile, Comments, Blogs


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'login-input-style'
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'login-input-style'
    
    class Meta:
        model = UserProfile
        fields = ('text', 'image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.blogname = kwargs.pop('blogname')
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'login-input-style'

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.commentedBy = UserProfile.objects.get(user=self.request.user)
        comment.blog = Blogs.objects.get(name=self.blogname)
        if commit:
            comment.save()
        return comment


class BlogForm(forms.ModelForm):
    #  text entry for users
    # title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    # image = forms.ImageField(required=False, help_text="Upload a picture.")
    # text = forms.CharField(max_length=1000, help_text="Write here...")

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'login-input-style'

    class Meta:
        model = Blogs
        fields = ['title','image','text']

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data
    
    def save(self, commit=True):
        blog = super().save(commit=False)
        if commit:
            blog.save()
        return blog