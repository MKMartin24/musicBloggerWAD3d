from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse, resolve
from musicBlogger.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def index(request):
    context_dict = {}
    context_dict['message'] ="this is the index page"
    return render(request, 'musicBlogger/index.html', context=context_dict)
