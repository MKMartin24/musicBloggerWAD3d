from django.contrib import admin
from musicBlogger.models import Artist,Songs,UserProfile,Blogs,Comments
# Register your models here.

admin.site.register(Artist)
admin.site.register(Songs)
admin.site.register(UserProfile)
admin.site.register(Blogs)
admin.site.register(Comments)
