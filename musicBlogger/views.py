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

from musicBlogger.models import *
from musicBlogger.forms import UserForm, UserProfileForm, CommentForm, BlogForm


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
    newest_blogs = Blogs.objects.order_by('-date')[:4]
    print(newest_blogs)
    context_dict['newest_blogs'] = newest_blogs
    return render(request, 'musicBlogger/index.html', context=context_dict)


def about(request):
    context_dict = {}
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
        context_dict = {}

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('musicBlogger:index'))
            else:
                context_dict['error_message']="Your Music Blogger account is disabled."
        else:
            print(f"Invalid login details: {username}, {password}")
            context_dict['error_message']="Invalid login details supplied."

    return render(request, 'musicBlogger/login.html',context=context_dict)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('musicBlogger:index'))


def search_blogs(request):
    context_dict = {}
    return render(request, 'musicBlogger/searchBlogs.html', context=context_dict)



def contact_us(request):
    context_dict = {}
    return render(request, 'musicBlogger/contact_us.html', context=context_dict)



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
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()
            registered = True
        else:
            context_dict['error_message']= user_form.errors+"/n"+profile_form.errors
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'musicBlogger/new_account.html', context=context_dict)

@login_required
def add_comment(request, slug):
    blog = Blogs.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commentedBy = UserProfile.objects.get(user = request.user)
            comment.blog = blog
            comment.save()
            blog_result = get_object_or_404(Blogs, slug=slug)
            return redirect('musicBlogger:blog', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'musicBlogger/add_comment.html', {'blog': blog, 'form': form})


@login_required
def write_blog(request):
    context_dict = {}
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.postedBy = UserProfile.objects.get(user=request.user)
            if 'image' in request.FILES:
                blog.image = request.FILES['image']
            blog.save()
            return redirect('musicBlogger:index')
        else:
            context_dict['error_message'] = form.errors
            print(form.errors)
    else:
        form = BlogForm()

    context_dict['form'] = form
    return render(request, 'musicBlogger/writeBlog.html', context=context_dict)

def profile(request, username, query = None):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    liked_song = profile.likedSong.all()[:12]
    following = None
    if profile.follows:
        following = User.objects.filter(id__in=profile.follows)
    else:
        following = User.objects.filter(id__in=[])
    id = profile.user.id
    not_followers = UserProfile.objects.exclude(follows__exact=[id])
    allUsers = UserProfile.objects.all()

    blogs = Blogs.objects.filter(postedBy=profile)[:12]
    num_following = following.count()
    num_followers = allUsers.count()-not_followers.count()
    following = UserProfile.objects.filter(user__in=following)[:12]
    context = {'profile': profile, "liked_song":liked_song,"following":following, "blogs":blogs, "num_followers":num_followers, "num_following":num_following}
    if request.user.is_authenticated:
        login_user = get_object_or_404(UserProfile, user=request.user)
        context['likedSongs'] = login_user.likedSong.all()
        context['alreadyFollowing'] = None
        if login_user.follows:
            if user.id in login_user.follows:
                context['alreadyFollowing'] =  request.user
            
        
    return render(request, 'musicBlogger/profile.html', context)

def view_blog(request, slug):
    blog_result = get_object_or_404(Blogs, slug=slug)
    comments = Comments.objects.filter(blog=blog_result)
    context_dict = {'blog':blog_result, 'comments':comments}
    return render(request, 'musicBlogger/viewBlog.html', context=context_dict)    

def search_page(request, query=None):
    results_songs,results_profiles,results_blogs = None,None,None
    try:
        query = request.GET['query']
        if len(query) > 0:
            results_profiles = UserProfile.objects.filter(
            Q(user__username__icontains=query)
            )[:12]
            results_songs = Songs.objects.filter(
            Q(name__icontains=query)
            )[:12]
            results_blogs = Blogs.objects.filter(
            Q(title__icontains=query)
            )[:12]
        else:
            results_songs = Songs.objects.all()[:12]
            results_profiles = UserProfile.objects.all()[:12]
            results_blogs = Blogs.objects.all()[:12]

        context_dict = {'results_songs': results_songs, 'results_profiles': results_profiles,'results_blogs': results_blogs}
        if request.user.is_authenticated:
            login_user = get_object_or_404(UserProfile, user=request.user)
            context_dict['likedSongs'] = login_user.likedSong.all()
        print(context_dict, query)
        return render(request, 'musicBlogger/search_results.html', context_dict)
    except KeyError:
        results_songs = Songs.objects.all()[:12]
        results_profiles = UserProfile.objects.all()[:12]
        results_blogs = Blogs.objects.all()[:12]
        context_dict = {'results_songs': results_songs, 'results_profiles': results_profiles,'results_blogs': results_blogs}
        if request.user.is_authenticated:
            login_user = get_object_or_404(UserProfile, user=request.user)
            context_dict['likedSongs'] = login_user.likedSong.all()
        return render(request, 'musicBlogger/search.html', context_dict)

   
def follow(request, username):
    try:
        current_pageUser = get_object_or_404(User, username=username)
        current_userProfile = get_object_or_404(UserProfile, user=request.user)
        if current_userProfile.follows is None:
            current_userProfile.follows = [current_pageUser.id]
            current_userProfile.save()
            response_data = {'results': 0}
            return JsonResponse(response_data)
        elif current_pageUser.id not in current_userProfile.follows:
            current_userProfile.follows.append(current_pageUser.id)
            current_userProfile.save()
            response_data = {'results': 0}
            return JsonResponse(response_data)
        else:
            current_userProfile.follows.remove(current_pageUser.id)
            current_userProfile.save()
            response_data = {'results': 1}
            return JsonResponse(response_data)
    except KeyError:
        response_data = {'results': 2}
        return JsonResponse(response_data)

    




def like(request):
    try:
        id = request.GET['id']
        username = request.GET['username']
        if len(id) > 0 and len(username)>0:
            current_user = get_object_or_404(User, username=username)
            current_userProfile = get_object_or_404(UserProfile, user=current_user)
            song = get_object_or_404(Songs, id=id)
            if current_userProfile.likedSong.filter(id=id).exists():
                current_userProfile.likedSong.remove(song)
                response_data = {'results': 0}
                return JsonResponse(response_data)
            else:
                current_userProfile.likedSong.add(song)
                response_data = {'results': 1}
                return JsonResponse(response_data)
    except KeyError:
        response_data = {'results': 2}
        return JsonResponse(response_data)
    response_data = {'results': 2}
    return JsonResponse(response_data)