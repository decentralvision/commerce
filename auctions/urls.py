from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<str:title>/", views.show, name="show"),
    path("auction/new", views.new, name="new"),
    path("category/<str:name>/", views.category, name="category"),
    path("categories", views.categories, name="category"),

    #dynamic page
    path("", views.index, name="index"),
    #auth req
    path("new", views.register, name="new"),
    path("watchlist", views.watchlist, name="watchlist"),
    path('admin/', admin.site.urls)
]
