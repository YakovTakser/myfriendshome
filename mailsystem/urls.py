from django.urls import path

from .import views

urlpatterns = [

    path('chat/', views.chat, name='chat'),
    path('conversation/<int:pk>/', views.conversation, name='conversation'),
]
