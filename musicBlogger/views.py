from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def index(request):
    context_dict = {}
    context_dict['message'] ="this is the index page"
    return render(request, 'musicBlogger/index.html', context=context_dict)

def about(request):
    context_dict = {}
    context_dict['message']="This is the about page"
    return render(request, 'musicBlogger/about.html', context=context_dict)

def login(request):
    context_dict = {}
    context_dict['message'] ="This is the login page"
    return render(request, 'musicBlogger/login.html', context=context_dict)

def search(request):
    context_dict = {}
    context_dict['message'] ="This is the search page"
    return render(request, 'musicBlogger/searchBlogs.html', context=context_dict)

def add_blog(request, blog_name_slug):
    context_dict = {}
    context_dict['message'] ="This is the add blog page"
    return render(request, 'musicBlogger/add_blog.html', context=context_dict)

def view_blog(request):
    context_dict = {}
    context_dict['message'] ="This is the view blog page"
    return render(request, 'musicBlogger/viewBlog.html', context=context_dict)

def contact_us(request):
    context_dict = {}
    context_dict['message'] ="This is the contact us page"
    return render(request, 'musicBlogger/contact_us.html', context=context_dict)

def profile(request):
    context_dict = {}
    context_dict['message'] ="This is the profile page"
    return render(request, 'musicBlogger/profile.html', context=context_dict)

def login(request):
    context_dict = {}
    context_dict['message'] ="This is the login page"
    return render(request, 'musicBlogger/login.html', context=context_dict)

def new_account(request):
    context_dict = {}
    context_dict['message'] ="This is the new account page"
    return render(request, 'musicBlogger/new_account.html', context=context_dict)