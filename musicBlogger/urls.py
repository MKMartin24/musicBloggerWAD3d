from django.urls import path
from musicBlogger import views

app_name = "music blogger"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name='about'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),

]
