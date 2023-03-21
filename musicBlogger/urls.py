from django.urls import path
from musicBlogger import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "musicBlogger"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name='about'),
    path('login/', views.user_login, name='login'),
    path('search/', views.search_page, name='search'),
    path('search/<str:query>/', views.search_page, name='search'),
    path('new_account/', views.new_account, name='new_account'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('logout/',views.user_logout, name="logout"),
    path('write_blog',views.write_blog,name='write_blog'),
    path('profile/<username>/', views.profile, name='profile'),
    path('profile', views.profile, name='profile'),
    path('blog/<blogname>/', views.view_blog, name='blog'),
    path('blog', views.view_blog, name='blog'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
