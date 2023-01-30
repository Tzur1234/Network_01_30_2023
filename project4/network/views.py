import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Import pagination classes
from django.core.paginator import Paginator

from .models import User, Post



@csrf_exempt
@login_required
def following(request, page_index):
    if request.method == 'GET':
        posts = Post.objects.filter(user__in=request.user.follow_others.all())
        posts = posts.order_by("-date").all()
        posts = [post.serialize(request.user) for post in posts]

        # Paginate
        p = Paginator(posts, 10)
        posts = p.get_page(page_index)

        return render(request, 'network/following.html', {
            "posts": posts
        })
    

@csrf_exempt
@login_required
def setFollow(request):
    if request.method == 'PUT':

        # retrieve the data
        data = json.loads(request.body)
        desire_follow_state = data['desire_follow_state']
        # the user we want to follow or unfollow
        user_id = data['user_id']
        user = User.objects.get(pk=user_id) 
        print(desire_follow_state)
        print(user.username)
        
        # Follow user
        if desire_follow_state:
            request.user.follow_others.add(user)
        # Unfollow user
        else:
            request.user.follow_others.remove(user)
        
        request.user.save()

        following = user.follow_others.all().count()
        followers = user.follow_me.count()

        return JsonResponse({"message": "follow has uppdated succesfuly", "following": following, "followers":followers }, status=200)


        

    # else:
    #     return JsonResponse({"message": "only PUT request you cna use"}, status=400)


# Return user profile
def profile(request, user_id, page_index):
    if request.method == 'GET':
        # Retrieve all of the user's posts
        user = User.objects.get(pk=user_id)
        # get all of the user's posts
        posts = Post.objects.filter(user=user)
        # Order posts by time
        posts = posts.order_by("-date").all()
        # convert to arr
        posts = [post.serialize(request.user) for post in posts]

        # Paginate
        p = Paginator(posts, 10)
        posts = p.get_page(page_index)

        # Number of users he follow / Follo by
        follow_others_count = user.follow_others.all().count()
        follow_user_count = user.follow_me.count()

        # user logged in
        follow_button = None
        print(f"{request.user.id}")
        if request.user.is_authenticated:
            # the request is from the user itself
            if user == request.user:
                follow_button = None
            elif user in request.user.follow_others.all():
                # user already followed
                follow_button = False
            else:
                follow_button = True
            
        
        
                 
        return render(request, 'network/profile.html', {
            "follow_button":follow_button,
            "posts":posts,
            "following":follow_others_count,
            "followers":follow_user_count,
            "username":user.username,
            "user_id": user.id,
            "img_url": user.img_url
        })



# API edit post
@csrf_exempt
@login_required
def editpost(request):
    if request.method == 'POST':
        #  Retrieve the data
        data = json.loads(request.body)
        post_id = int(data['post_id'])
        new_content = data['new_content']

        print(post_id)
        print(new_content)

        # Validate This is the write user
        post = Post.objects.get(pk=post_id)

        # only onwer user can edit the post
        if post.user != request.user:
            return JsonResponse({"message": 'only onwer user can edit the post'}, status=400)


        # update data
        post.content = new_content
        post.save()

        return JsonResponse({"message":"Post has updated succesfuly"}, status=200 )


    else:
        return JsonResponse({"message": 'Only POST request allowd to this route'}, status=400)



# API - create post
@csrf_exempt
@login_required
def addpost(request):
    # check the method
    if request.method == 'POST':
    # Retrieve the data
        data = json.loads(request.body)
        content = data['content']
        print(content)

    # Insert the data into DB
        newPost = Post(user=request.user, content=content)
        newPost.save()

    # return the post
        return JsonResponse([newPost.serialize(request.user)], safe=False)

    else:
        return JsonResponse({'message': 'addpost except only POST requests'}, status=400)



# API - return all of the posts
def allposts(request, page_index):
    

    if(request.method == 'GET'):
        posts = Post.objects.all()

        
        # order the posts accorsing to the data
        posts = posts.order_by("-date").all()

        # Paginate all the pots
        p = Paginator(posts, 10)
        
        # Pick the posts from the page_index
        posts = p.get_page(page_index)
        
        posts_arr = [post.serialize(request.user) for post in posts]


        # return list of dictionery - each one represents  post
        return JsonResponse(posts_arr, safe=False)


    
    else:
        return JsonResponse({"message": "GET request is required"}, status=400)

# add or remove the user from users_gave_like
@csrf_exempt
@login_required
def changelike(request):
    # check the request method
    if request.method == 'POST':
        # extract Json data
        data = json.loads(request.body)
        change_status_like_to = data["change_status_like_to"]
        post_id = int(data["post_id"])



        # get the post object
        post = Post.objects.get(pk=post_id)
        # Update like\unlike status in database
        if(change_status_like_to):
            post.users_gave_like.add(request.user)
            post.likes += 1
            print("change to like")
        else:
            post.users_gave_like.remove(request.user)
            post.likes -= 1
            print("change to unlike")

        # update
        post.save()

        # return the updated number of likes
        return JsonResponse({"likes": f"{post.likes}"}, status=200)
    
    # update like must be via PUT request
    else:
        return JsonResponse({"error": "POST request required."}, status=400, safe=False)



def index(request):

    return render(request, "network/index.html")


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
