
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # profile page
    path("profile/<int:user_id>/<int:page_index>", views.profile, name='profile'),
    # Show the people you follow
    path("following/<int:page_index>", views.following, name='following'),
    


    # API
    path("allposts/<int:page_index>", views.allposts, name="posts"),
    path("changelike", views.changelike, name="changelike"),
    path("addpost", views.addpost, name="addpost"),
    path("editpost", views.editpost, name="editpost"),
    path("setFollow", views.setFollow, name="setFollow")


]
