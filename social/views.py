from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "social/register.html", {"form": form})
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(request, "social/login.html", {"form": form})
def home(request):
    posts = Post.objects.all().order_by("-created_at")

    following_users = []

    if request.user.is_authenticated:
        following_users = Follow.objects.filter(
            follower=request.user
        ).values_list("following_id", flat=True)

    return render(
        request,
        "social/home.html",
        {
            "posts": posts,
            "following_users": following_users
        }
    )
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Follow


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Post.objects.create(
                user=request.user,
                content=content
            )

        return redirect("home")

    return render(request, "social/create_post.html")
@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        content = request.POST.get("content")

        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )

    return redirect("home")


@login_required
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("home")
@login_required
def toggle_follow(request, user_id):
    user_to_follow = User.objects.get(id=user_id)

    if user_to_follow != request.user:

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()

    return redirect("home")
def profile(request, user_id):
    profile_user = User.objects.get(id=user_id)

    posts = Post.objects.filter(
        user=profile_user
    ).order_by("-created_at")

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()
    
    return render(
        request,
        "social/profile.html",
        {
            "profile_user": profile_user,
            "posts": posts,
            "followers_count": followers_count,
            "following_count": following_count,
        }
    )