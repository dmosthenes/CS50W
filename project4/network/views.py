from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.forms import ModelForm, TextInput, FileInput, Textarea
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

from .models import User, Follow, Post, Like, Reply
from django.db.models import Q


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio", "location", "work", "picture"]
        widgets = {
            "first_name": TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            "last_name": TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            "picture": FileInput(attrs={'class': 'form-control'}),
            "bio": Textarea(attrs={'placeholder': 'Bio', 'class': 'form-control'}),
            "location": TextInput(attrs={'placeholder': 'Home', 'class': 'form-control'}),
            "work": TextInput(attrs={'placeholder': 'Job', 'class': 'form-control'})}
        labels = {
            'first_name': False,
            'last_name': False,
            'picture': False,
            'bio': False,
            'location': False,
            'work': False
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({
            'class': 'form-control-file btn-primary-btn',
            'id': 'customFile',
            'aria-describedby': 'customFileLabel'

        })


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["body"]
        widgets = {
            "body": Textarea(attrs={'placeholder': 'What\'s happening?', 'class': 'post-box form-control', 'required': True})
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


def index(request):

    page_obj = (None, None, None)

    if request.user.is_authenticated:

        # Get paginator object for all posts on network
        page_obj = listing(request)

        if len(page_obj) == 0:
            page_obj = (None, None, None)

    return render(request, "network/index.html", {

        "page_obj": page_obj[0],
        "likes": page_obj[1],
        "already_liked": page_obj[2],
        "post_form": PostForm(),
        "reply_form": ReplyForm()

    })

def listing(request, users=None, profile=None):

    # Get the page number
    page = 1 if request.GET.get("page", None) is None else request.GET["page"]

    if not users and not profile:

        # Get posts for everyone
        posts = Post.objects.all().order_by('-timestamp')

    elif profile:

        # Get posts for profile user only
        posts = Post.objects.filter(poster=profile).order_by('-timestamp')

    else:

        # Get all posts from followeds and sort from newest to oldest
        posts = Post.objects.filter(Q(poster__in=users)).order_by('-timestamp')

    p = Paginator(posts, 10)

    likes = get_likes(request, p.page(page))

    return (p.page(page), likes[0], likes[1])

@login_required
def get_user(request):

    user_data = {
        "id": request.user.id,
        "username": request.user.username
    }

    return JsonResponse({
        "user": user_data
    })

@login_required
@csrf_exempt
def post(request):

    # Create the post in the database
    if request.method == "POST":
        data = json.loads(request.body)

        user = User.objects.get(id=data["user"])

        post = Post.objects.create(poster=user, body=data["comment"])

        # TODO: can't like new posts without refresh

        new_post = render(request, "network/post.html", {
            "post": post,
            "user": user,
            "likes": {post.id: 0},
            "already_liked": {post.id: False},

        })

        # Return the database object for the post
        return HttpResponse(new_post)
    
    return JsonResponse({
        "message": "Not posted successfully"})

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

     # Get all followeds of user
    followeds = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)

    # Get posts for only users being followed
    if followeds:

        # Get paginator object for posts of followeds
        page_obj = listing(request, followeds)

        # Get all follows by current user
        follower = User.objects.get(username=str(request.user))
        user_follows = Follow.objects.filter(follower=follower)

        # Create list of following users
        followings = [User.objects.get(username=follow.followed.username) for follow in user_follows]

        return render(request, "network/following.html", {
            "followed_users": followings,
            "page_obj": page_obj[0],
            "likes": page_obj[1],
            "already_liked": page_obj[2]
        })
    
    # If user is not following anyone, display no posts
    else:

        return render(request, "network/following.html", {
            "followed_users": None,
            "page_obj": None,
            "likes": None,
            "already_liked": None
        })

def profile_view(request, user):

    # Get user profile
    # profile = User.objects.get(username=user)
    profile = get_object_or_404(get_user_model(), username=user)

    # Get user's posts paginator object
    page_obj = listing(request, None, profile)

    # Check if logged in user is following loaded user
    follower = User.objects.get(username=str(request.user))
    followed = Follow.objects.filter(follower=follower,followed=profile).exists()

    if request.method == "POST":

        # Update user model
        # profile_form = UserForm(request.POST, request.FILES, instance=profile)

        # print(profile_form.fields["picture"].url)

        # if profile_form.is_valid():

        #     profile_form.save()

        # Update the fields in the user's profile
        profile.last_name = request.POST.get('last_name')
        profile.first_name = request.POST.get('first_name')
        profile.work = request.POST.get('work')
        profile.location = request.POST.get('location')
        profile.bio = request.POST.get('bio')

        # Update image if available
        if len(request.FILES) != 0:
            profile.picture = request.FILES['picture']

        profile.save()
     
    profile_form = UserForm(instance=profile)

    print(profile.picture)
    
    return render(request, "network/profile.html", {
        "profile_form": profile_form,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "work": profile.work,
        "location": profile.location,
        "bio": profile.bio,
        "picture": profile.picture,
        "is_own_profile": str(request.user) == user,
        "following": followed,
        "profile_user": user,
        "page_obj": page_obj[0],
        "likes": page_obj[1],
        "already_liked": page_obj[2]
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


def get_likes(request, posts):

    # posts parameter is a paginator object
    # Get all post ids
    if posts.object_list:
        post_ids = [post.id for post in posts.object_list]

        # Get like counts for each post id
        likes = {id:
                Like.objects.filter(post=id).count() for id in post_ids or 0}
        
        # Get whether user has liked already
        already_liked = {id:
                        Like.objects.filter(post=id, liker=request.user).exists() for id in post_ids}

        return (likes, already_liked)

    return (None, None)

@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Get the post object
        post = Post.objects.get(id=data["post-id"])

        # Check if a Like already exists from user to post
        if Like.objects.filter(liker=request.user, post=post).exists():

            # Delete the like (un-like)
            Like.objects.get(liker=request.user, post=post).delete()

        else:

            # Create a Like from current user to post-id
            Like.objects.create(liker=request.user, post=post)

        # Count the number of likes on the post
        likes = Like.objects.filter(post=post).count()

        return JsonResponse({
            "count": likes
        })
    
@login_required
@csrf_exempt
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)

        post_id = data["post_id"]
        new_post = data["new_content"]

        # Get comment object
        post = Post.objects.get(id=post_id)

        # Update body field
        post.body = new_post

        post.save()

        return JsonResponse({
            "post": post.body
        })

    return JsonResponse({"error": "Bad request"}, status=400)



