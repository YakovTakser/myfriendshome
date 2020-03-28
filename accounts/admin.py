from django.contrib import admin
from .models import Profile, FriendRequest, Conversation, Message

# Register your models here.

admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Conversation)
admin.site.register(Message)
