from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, TextInput, FileInput, Textarea
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


from .models import User, Follow, Post, Like, Reply


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "picture", "bio", "location", "work"]
        widgets = {
            "first_name": TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            "last_name": TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            "picture": FileInput(attrs={'class': 'form-control'}),
            "bio": Textarea(attrs={'placeholder': 'Bio', 'class': 'form-control'}),
            "location": TextInput(attrs={'placeholder': 'Home', 'class': 'form-control'}),
            "work": TextInput(attrs={'placeholder': 'Job', 'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({
            'placeholder': 'Display Picture',
            'class': 'form-control'
        })

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["body"]
        widgets = {
            "body": Textarea(attrs={'placeholder': 'What\'s happening?', 'class': 'form-control'})
        }
        labels = {
            "body": ""
        }
        label_suffix = {
            ''
        }

class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ["body"]
        widgets = {
            "body": Textarea(attrs={'placeholder': 'Reply', 'class': 'form-control'})
        }

@login_required
def index(request):

    # Get all posts for user and follows

    return render(request, "network/index.html", {
        "posts": "pass",
        "post_form": PostForm(),
        "reply_form": ReplyForm()

    })

def post(request):
    pass

@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)

        follower = User.objects.get(username=data["follower"])
        followed = User.objects.get(username=data["followed"])

        # Unfollowing if following
        if data["following"] == "True":
            Follow.objects.filter(follower=follower, followed=followed).delete()
            return JsonResponse({'message': "Unfollowed successfully"})

        # Follow otherwise
        else:
            Follow.objects.create(follower=follower, followed=followed)
            return JsonResponse({"message": "Followed successfully"})


def following_view(request):

    # Get all follows by current user
    follower = User.objects.get(username=str(request.user))
    user_follows = Follow.objects.filter(follower=follower)

    # Create list of following users
    followings = [User.objects.get(username=follow.followed.username) for follow in user_follows]

    return render(request, "network/following.html", {
        "followed_users": followings
    })

def profile_view(request, user):

    # Get user profile
    profile = User.objects.get(username=user)

    # Get user followers

    # followers = Follow.objects.get(followed=profile)

    # Check if logged in user is following loaded user
    follower = User.objects.get(username=str(request.user))
    followed = Follow.objects.filter(follower=follower,followed=profile).exists()

    if request.method == "POST":

        # Update user model
        profile_form = UserForm(request.POST, instance=profile)
        if profile_form.is_valid():

            profile_form.save()
    
    else:

        profile_form = UserForm(instance=profile)

    return render(request, "network/profile.html", {
        "profile_form": profile_form,
        "is_own_profile": str(request.user) == user,
        "following": followed,
        "profile_user": user
        # "folllowers": followers
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
