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

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.commentedBy = UserProfile.objects.get(user=self.request.user)
        comment.blog = Blogs.objects.get(name=self.blogname)
        if commit:
            comment.save()
        return comment