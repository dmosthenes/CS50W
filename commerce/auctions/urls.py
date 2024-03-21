from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>/", views.category, name="category"),
    path("<str:listing_id>", views.listing, name="listing"),
    path("<str:listing_id>/", views.add_to_watchlist, name="add_to_watchlist"),
    path("<str:listing_id>/<str:winner>", views.close_listing, name="close_listing"),
    path("<str:listing_id>", views.close_listing, name="close_listing")


]
