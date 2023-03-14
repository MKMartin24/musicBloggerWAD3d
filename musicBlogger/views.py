from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def index(request):
    context_dict = "this is the index page"
    return render(request, 'musicBlogger/index.html', context=context_dict)

def about(request):
    context_dict = "This is the about page"
    return render(request, 'musicBlogger/about.html', context=context_dict)

def login(request):
    context_dict = "This is the login page"
    return render(request, 'musicBlogger/login.html', context=context_dict)

def search(request):
    context_dict = "This is the search page"
    return render(request, 'musicBlogger/search.html', context=context_dict)

def add_blog(request, blog_name_slug):
    context_dict = "This is the add blog page"
    return render(request, 'musicBlogger/add_blog.html', context=context_dict)

def view_blog(request):
    context_dict = "This is the view blog page"
    return render(request, 'musicBlogger/viewBlog.html', context=context_dict)