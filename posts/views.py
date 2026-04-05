from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, NewUserForm, PasswordResetFormPrintToken
from .models import Comment, Post


def blog_list(request):
    blogs = Post.objects.all()
    return render(request, "posts/blog_list.html", {"blogs": blogs})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be signed in to add a comment.")
            return redirect("post-detail", post_id=post.id)
        content = request.POST.get("content", "").strip()
        if content:
            Comment.objects.create(blog=post, content=content)
            messages.success(request, "Your comment was posted.")
        else:
            messages.warning(request, "Comment cannot be empty.")
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
            messages.success(
                request,
                "Account created successfully. You can log in now.",
            )
            return redirect("login")
        messages.error(
            request,
            "Registration could not be completed. Please fix the errors below.",
        )
    else:
        form = NewUserForm()
    return render(request, "auth/register.html", {"form": form})


def login_request(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_username()}!")
                return redirect("blog-list")
        messages.error(
            request,
            "Login failed. Check your username and password and try again.",
        )
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def logout_request(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("blog-list")


class PasswordResetWithToastView(SuccessMessageMixin, PasswordResetView):
    form_class = PasswordResetFormPrintToken
    template_name = "auth/password_reset_form.html"
    success_url = reverse_lazy("password_reset_done")
    success_message = (
        "If that email is registered, the reset link was printed in the server terminal."
    )

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please enter a valid email address.",
        )
        return super().form_invalid(form)


class PasswordResetConfirmWithToastView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")
    success_message = "Your password was updated. You can log in now."

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Could not update your password. Check the requirements below.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get("validlink") is False:
            messages.error(
                self.request,
                "This password reset link is invalid or has already been used.",
            )
        return context
