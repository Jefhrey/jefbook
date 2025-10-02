from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from .models import Post, User, Comment, Like
from django.views.decorators.http import require_POST


class NewPost(forms.Form):
    title = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control w-50 me-auto my-2 ms-1"
            }
        )
    )

    content = forms.CharField(
        widget = forms.Textarea(
            attrs={
                "autocomplete": "off"
            }
        )
    )

from .models import User


def index(request):
    posts = Post.objects.all()
    print("HELLLLOOOOOO")
    print(posts)
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create(request):
    if request.method == "POST":
        form = NewPost(request.POST)
        if form.is_valid():
            response = form.cleaned_data
            # tit = 
            # cont = 
            new_post = Post(
                title = response["title"],
                content = response["content"],
                poster = request.user 
            )
            new_post.save()
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "network/create.html", {
        "post": NewPost()
    })

def profile(request, id):
    return render(request, "network/profile.html", {
        "id" : id
    })

@require_POST
def update_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status = 401)
    current_post = get_object_or_404(Post, id=post_id)
    # create new like
    if(request.user in current_post.likes.all()):
        # post has been liked already. Remove the like
        current_post.likes.remove(request.user)
    
    else:
        current_post.likes.add(request.user)
    
    return JsonResponse({
        "like_count": current_post.likes.count()
    })