from django.shortcuts import get_object_or_404, redirect, render
from .models import Comment, Post


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
