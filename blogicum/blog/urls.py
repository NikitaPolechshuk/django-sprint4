from django.urls import path
from django.contrib.auth import get_user_model

from . import views

User = get_user_model()

app_name = 'blog'

urlpatterns = [
    path('',
         views.PostListView.as_view(),
         name='index'),

    # Profile URLS
    path('profile/<str:username>/',
         views.UserPostListView.as_view(),
         name='profile'),
    path('edit_profile/',
         views.UserUpdateView.as_view(),
         name='edit_profile'),

    # Post URLS
    path('post/create/',
         views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),

    # Commet URLS
    path('posts/<int:post_id>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
    # Category URLS
    path('category/<slug:category_slug>/',
         views.CategoryPostListView.as_view(),
         name='category_posts'),
]
