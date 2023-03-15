from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, resolve
from musicBlogger.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def index(request):
    context_dict = {}
    context_dict['message'] ="this is the index page"
    return render(request, 'musicBlogger/index.html', context=context_dict)

def about(request):
    context_dict = {}
    context_dict['message']="This is the about page"
    return render(request, 'musicBlogger/about.html', context=context_dict)

def styling_function(request, add_to_recent, context_dict):

    if(add_to_recent):
        context_dict["page"] = "musicBlogger:" + resolve(request.path_info).url_name
        recent = request.COOKIES.get("recent")
        if(recent):
            context_dict["recent"] = recent.split(",")

    try:
        username = request.user.username
        user_data = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user_data)
        context_dict["profile_picture"] =  user_profile.picture
    except: #User does not exist
        pass

def login(request):
    context_dict = {}
    context_dict['message'] ="This is the login page"
    styling_function(request, True, context_dict)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password) # Checks if valid password.
 
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('musicBlogger:index'))
            else:
                return HttpResponse("Your musicBlogger account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    else:
        return render(request, 'musicBlogger/login.html', context=context_dict)


@login_required
def logout(request):
    logout(request)
    return redirect(reverse('musicBlogger:index'))

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



def new_account(request):
    context_dict = {}
    context_dict['message'] ="This is the new account page"
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # Save user form data to databse
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})
