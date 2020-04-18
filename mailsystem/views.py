from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
#####################################################
# Chat
#####################################################

# Shows all chats of the user
from .models import Conversation, Message


@login_required()
def chat(request):
    # Start empty query set
    conversations = Conversation.objects.none()
    # Take all conversation of current user
    conversations1 = Conversation.objects.filter(user1=request.user)
    conversations2 = Conversation.objects.filter(user2=request.user)
    # Merge between the query sets
    conversations = conversations1 | conversations2
    context = {'conversations': conversations}
    return render(request, 'accounts/chat.html', context)


# Shows all messages of a specific chat of the user
@login_required()
def conversation(request, pk):
    current_conversation = get_object_or_404(Conversation, pk=pk)
    # check if user is the owner of the conversion
    if request.user != current_conversation.user1 and request.user != current_conversation.user2:
        raise Http404("Page does not exist")

    if request.method == 'POST':
        msg = request.POST.get('msg')
        if current_conversation.user1 == request.user:
            message = Message.objects.create(sender=request.user, receiver=current_conversation.user2, text=msg)
        else:
            message = Message.objects.create(sender=request.user, receiver=current_conversation.user1, text=msg)
        message.save()
        current_conversation.messages.add(message)

    messages = current_conversation.messages.all()
    # Start empty query set
    conversations = Conversation.objects.none()
    # Take all conversation of current user
    conversations1 = Conversation.objects.filter(user1=request.user)
    conversations2 = Conversation.objects.filter(user2=request.user)
    # Merge between the query sets
    conversations = conversations1 | conversations2

    context = {
        'current_conversation': current_conversation,
        'conversations': conversations,
        'messages': messages,
    }
    return render(request, 'accounts/conversation.html', context)