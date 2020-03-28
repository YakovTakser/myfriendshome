from django.urls import path

from . import views



urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('', views.PostList, name='post_list'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/remove', views.PostDeleteView.as_view(), name='post_remove'),
    # Addition functionality routs to posts
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('liketopost/<int:pk>/', views.like_to_post, name='like_to_post'),
    path('unliketopost/<int:pk>/', views.unlike_to_post, name='unlike_to_post'),


]