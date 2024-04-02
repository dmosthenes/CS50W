from django.contrib import admin
from .models import Follow, User, Post, Reply, Like

# Register your models here.
admin.site.register(Follow)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Like)
