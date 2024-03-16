from django.contrib import admin
from .models import Listing, Bids, Comments, User, Category

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Category)