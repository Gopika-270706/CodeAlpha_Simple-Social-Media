from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("",views.home, name="home"),
    path("create_post",views.create_post, name="create_post"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("follow/<int:user_id>/", views.toggle_follow, name="toggle_follow"),
    path("profile/<int:user_id>/",views.profile, name="profile")
]