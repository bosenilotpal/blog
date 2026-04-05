"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetDoneView
from django.urls import path

from posts.views import (
    PasswordResetConfirmWithToastView,
    PasswordResetWithToastView,
    blog_list,
    login_request,
    logout_request,
    post_detail,
    register_request,
)

urlpatterns = [
    path('', blog_list, name='blog-list'),
    path('posts/<int:post_id>/', post_detail, name='post-detail'),
    path('admin/', admin.site.urls),
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path("logout", logout_request, name="logout"),
    path(
        "password-reset",
        PasswordResetWithToastView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmWithToastView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete",
        PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
