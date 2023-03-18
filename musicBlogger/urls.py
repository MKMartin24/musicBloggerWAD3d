from django.urls import path
from musicBlogger import views

app_name = "music blogger"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name='about'),
    path('profiles/<int:profile_id>/', views.profile, name='profile'),
]
