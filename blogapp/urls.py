from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("post_article/",views.post,name="post_article"),
    path("post_details/<uuid:id>/",views.post_details,name="post_details"),
    path("edit_article/<uuid:id>/",views.edit_post,name="edit_article"),
    path("register/",views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('adminpage/',views.adminpage,name="admin"),
    path('change_password/', views.change_password, name='change_password'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"),name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),
    path('',views.index,name='index'),
    path("search/",views.search,name="search"),
    path('like/<uuid:id>/',views.like_post,name='like-post'),
    path('comment_post/<uuid:id>/',views.comment_post,name='comment-post'),
]
