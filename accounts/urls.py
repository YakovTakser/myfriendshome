from django.contrib.auth import views as auth_views
from django.urls import path
from .import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profilewatch/<int:pk>/', views.profile_watch, name='profile_watch'),
    path('sendfriendrequest/<int:pk>/', views.send_friend_request, name='send_friend_request'),
    path('cancelfriendrequest/<int:pk>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('acceptfriendrequest/<int:pk>/', views.accept_friend_request, name='accept_friend_request'),
    path('deletefriendrequest/<int:pk>/', views.delete_friend_request, name='delete_friend_request'),
    path('deletefriend/<int:pk>/', views.delete_friend, name='delete_friend'),
    path('friends/', views.friends, name='friends'),
    path('findfriends/', views.find_friends, name='find_friends'),
]