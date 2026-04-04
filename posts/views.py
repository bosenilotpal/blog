from django.shortcuts import get_object_or_404, redirect, render
from .models import Comment, Post
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import NewUserForm, LoginForm

def blog_list(request):
    blogs = Post.objects.all()
    return render(request, "posts/blog_list.html", {"blogs": blogs})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Comment.objects.create(blog=post, content=content)
        return redirect("post-detail", post_id=post.id)

    comments = Comment.objects.filter(blog=post).order_by("-created_at")
    context = {
        "post": post,
        "comments": comments,
    }
    return render(request, "posts/post_detail.html", context)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    form = NewUserForm()
    return render(request, "auth/register.html", {"form": form})


def login_request(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("blog-list")
    form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def logout_request(request):
    logout(request)
    return redirect("blog-list")