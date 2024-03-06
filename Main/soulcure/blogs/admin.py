from django.contrib import admin
from .models import BlogCategory,Posts,PostView,Comment
# Register your models here.

admin.site.register(BlogCategory)
admin.site.register(Posts)
admin.site.register(PostView)
admin.site.register(Comment)
