from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def index(request):
    context_dict = {"text":"this is the index page"}
    return render(request, 'musicBlogger/index.html', context=context_dict)

def about(request):
    context_dict = {}
    return render(request, 'musicBlogger/about.html',context=context_dict)