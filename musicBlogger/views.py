from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, resolve
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
import json

from musicBlogger.models import UserProfile,Artist,Songs,Blogs,Comments,User
from musicBlogger.forms import UserForm, UserProfileForm


# Create your views here.
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits


def index(request):
    context_dict = {}
    context_dict['message'] = "this is the index page"
    return render(request, 'musicBlogger/index.html', context=context_dict)


def about(request):
    context_dict = {}
    context_dict['message'] = "This is the about page"
    return render(request, 'musicBlogger/about.html', context=context_dict)


def styling_function(request, add_to_recent, context_dict):
    if (add_to_recent):
        context_dict["page"] = "musicBlogger:" + resolve(request.path_info).url_name
        recent = request.COOKIES.get("recent")
        if (recent):
            context_dict["recent"] = recent.split(",")

    try:
        username = request.user.username
        user_data = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user_data)
        context_dict["profile_picture"] = user_profile.picture
    except:  # User does not exist
        pass


def user_login(request):
    context_dict = {}
    styling_function(request, True, context_dict)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)  # Checks if valid password.

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('musicBlogger:index'))
            else:
                return HttpResponse("Your Music Blogger account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'musicBlogger/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('musicBlogger:index'))


def search_blogs(request):
    context_dict = {}
    return render(request, 'musicBlogger/searchBlogs.html', context=context_dict)


def add_blog(request, blog_name_slug):
    context_dict = {}
    return render(request, 'musicBlogger/add_blog.html', context=context_dict)


def view_blog(request):
    context_dict = {}
    return render(request, 'musicBlogger/viewBlog.html', context=context_dict)


def contact_us(request):
    context_dict = {}
    return render(request, 'musicBlogger/contact_us.html', context=context_dict)


def profile(request):
    context_dict = {}
    return render(request, 'musicBlogger/profile.html', context=context_dict)


def new_account(request):
    context_dict = {}
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # Save user form data to database
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.name = user
            if 'image' in request.FILES:
                profile.picture = request.FILES['image']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}

    return render(request, 'musicBlogger/new_account.html', context=context_dict)


@login_required
def write_blog(request):
    context_dictionary = {}
    return render(request, 'musicBlogger/writeBlog.html', context=context_dictionary)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, name=user)
    context = {'profile': profile}
    return render(request, 'musicBlogger/profile.html', context)
    

def search_page(request, query=None):

    try:
        query = request.GET['query']
        if len(query) > 0:
            results_profiles = UserProfile.objects.filter(
            Q(name__username__icontains=query)
            )
            
            results_songs = Songs.objects.filter(
            Q(name__icontains=query)
            )
            
            results_blogs = Blogs.objects.filter(
            Q(name__icontains=query)
            )
        else:
            results_songs = Songs.objects.all()
            results_profiles = UserProfile.objects.all()
            results_blogs = Blogs.objects.all()
        return  render(request, 'musicBlogger/search_results.html', {'results_songs': results_songs, 'results_profiles': results_profiles,'results_blogs': results_blogs})
    except KeyError:
        results_songs = Songs.objects.all()
        results_profiles = UserProfile.objects.all()
        results_blogs = Blogs.objects.all()
        return render(request, 'musicBlogger/search.html', {'results_songs': results_songs, 'results_profiles': results_profiles,'results_blogs': results_blogs})
   
    