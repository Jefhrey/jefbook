
from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("profile/<int:id>", views.profile, name = "profile"),
    path("like/<int:post_id>", views.update_like, name = "like"),
    path("follow/<int:user_id>", views.update_follow, name = "follow"),
    path("following", views.following, name = "following"),
    path("edit/<int:id>", views.edit, name = "edit")
]

