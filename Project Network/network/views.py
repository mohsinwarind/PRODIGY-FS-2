from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import User,Post,Follow,Comment
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def index(request):
    return redirect('all-posts')

def image(request):
    pass
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
    

def new_post(request):
    if request.method == "POST":
        content = request.POST.get('content')
        image  = request.FILES.get('image')
        post = Post(user = request.user , content = content)
        if image:
            post.image = image

        post.save()
        return redirect("index")
    return render(request, "network/new_post.html")


def all_posts(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj.object_list,
        'page_obj':page_obj,
        'edit_mode': False
    }
    
    return render(request, "network/all_posts.html",context)

@login_required
def profile_view(request,username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user= user_profile).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_following = Follow.objects.filter(follower = request.user , followed = user_profile).exists()

    if request.method == "POST":
        if is_following:
            Follow.objects.filter(follower= request.user , followed = user_profile).delete()
        else:
            Follow.objects.create(follower =request.user , followed = user_profile)
        return redirect('profile',username = username)
    
    context = {
        'user_profile': user_profile,
        'posts' : page_obj.object_list,
        'is_following': is_following,
        'page_obj':page_obj
    }
    return render(request , "network/profile.html", context)

@login_required
@require_POST
def edit_post(request , post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.user != request.user:
        return JsonResponse({"error": "You can't edit this post"},status=403)
    
    new_content = request.POST.get('content')

    if not new_content:
        return JsonResponse({"error": "Content can't be null"},status= 400)
    
    post.content = new_content
    post.save()

    return JsonResponse({"message" : "Post updated successfully", "content" : new_content})

@login_required
@require_POST
def like_unlike_post(request,post_id):
    try:
        post= Post.objects.get(id=post_id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            'liked' : liked,
            'like_count':post.likes.count()
        })
    except Post.DoesNotExist:
            return JsonResponse({'error':'Post does not exists'}, status = 404)
@login_required
def following_page(request):
    user = request.user
    
    followed_users_ids = Follow.objects.filter(follower=user).values_list('followed_id', flat=True)
    
    posts = Post.objects.filter(user_id__in=followed_users_ids).order_by('-timestamp')
    paginator = Paginator(posts,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html', {
        'posts': page_obj.object_list,
        'page_obj':page_obj
        })

def post_detail(request,id ):
    post = Post.objects.get(id = id)
    return render(request, 'network/post_detail.html',{'post' : post})


@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if not content:
            return JsonResponse({"error": "Comment cannot be empty."}, status=400)

        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(post=post, user=request.user, content=content)

        return JsonResponse({
            "id": comment.id,
            "user": comment.user.username,
            "content": comment.content,
            "timestamp": comment.timestamp.strftime("%b %d, %Y, %I:%M %p")
        })


@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        user = request.user
        user.profile_image = request.FILES['profile_image']
        user.save()

        return redirect('profile', username=user.username)

    return redirect('profile', username=request.user.username)