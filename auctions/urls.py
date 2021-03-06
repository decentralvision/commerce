from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<int:id>/", views.show, name="show"),
    path("category/<str:name>/", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    #dynamic page
    path("", views.index, name="index"),
    #auth req
    path("new", views.register, name="new"),
    path("bid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("admin/", admin.site.urls),
    path("comment", views.comment, name="comment"),
    path("auction/new", views.new, name="new"),
    path("auction/close/<int:id>", views.close, name="close")
]
