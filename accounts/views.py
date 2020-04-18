import shutil
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from .forms import UserCreateForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
import os
from django.conf import settings
from blog.models import Post, Image
from mailsystem.models import Conversation
from .models import FriendRequest


# Get and return an object or None



def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"




@login_required
def profile(request):
    # If method is POST
    if request.method == 'POST':
        img_profile_previous = request.user.profile.image
        img_theme_previous = request.user.profile.theme_image
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # IF PICTURE WAS CHANGED PUT IT TO THE USER PICS DIRECTORY
            if img_profile_previous != request.user.profile.image:
                image = pic_save(request, request.user.profile.image)
                request.user.profile.image = image
                request.user.profile.save()
            if img_theme_previous != request.user.profile.theme_image:
                image = pic_save(request, request.user.profile.theme_image)
                request.user.profile.theme_image = image
                request.user.profile.save()
            return redirect('profile')
    # If method is GET
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        friends = request.user.profile.friends.all()
        sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
        received_friend_requests = FriendRequest.objects.filter(to_user=request.user)
        posts_number = Post.objects.filter(author=request.user).count()
        friends_number = request.user.profile.friends.all().count()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'users': friends,
        'friends_label': 'My Friends',
        'sent_friend_requests': sent_friend_requests,
        'received_friend_requests': received_friend_requests,
        'posts_number': posts_number,
        'friends_number': friends_number,
    }
    return render(request, 'accounts/profile.html', context)


def profile_watch(request, pk):
    user_watch = get_object_or_404(User, pk=pk)

    if request.user.is_authenticated:
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'StartChat':
                # Check if the conversation between 2 users exists if yes then show it
                # if not then create it and after that show it
                con = get_or_none(Conversation, user1=request.user, user2=user_watch)
                if con:
                    pk_conversation = con.pk
                else:
                    con = get_or_none(Conversation, user1=user_watch, user2=request.user)
                    if con:
                        pk_conversation = con.pk
                    else:
                        pass
                        con = Conversation.objects.create(user1=request.user, user2=user_watch)
                        pk_conversation = con.pk
                return redirect('conversation', pk=pk_conversation)

    profile = user_watch.profile
    button_status = 'none'
    if request.user.is_authenticated:
        if profile not in request.user.profile.friends.all():
            button_status = 'not_friend'

            # if we have sent him a friend request
            if len(FriendRequest.objects.filter(
                    from_user=request.user).filter(to_user=profile.user)) == 1:
                button_status = 'friend_request_sent'
    context = {'user_profile': user_watch,
               'button_status': button_status,
               }
    print('friend status ' + str(button_status))
    return render(request, 'accounts/profile_watch.html', context)


###################################################
# Friends Views here
###################################################


def send_friend_request(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        frequest, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=user)
        context = {'user_profile': user}
        return redirect('profile_watch', pk)


def cancel_friend_request(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        frequest = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user).first()
        frequest.__str__()
        frequest.delete()
        context = {'user_profile': user}
        return redirect('profile_watch', pk)


@login_required()
def accept_friend_request(request, pk):
    from_user = get_object_or_404(User, pk=pk)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    frequest.delete()
    context = {'user_profile': from_user}
    return redirect('profile')


def delete_friend_request(request, pk):
    from_user = get_object_or_404(User, pk=pk)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    context = {'user_profile': from_user}
    return redirect('profile')


@login_required()
def delete_friend(request, pk):
    friend_delete = get_object_or_404(User, pk=pk)
    friend_delete.profile.friends.remove(request.user.profile)
    request.user.profile.friends.remove(friend_delete.profile)
    return redirect('profile_watch', pk)





@login_required()
def friends(request):
    return render(request, "accounts/friends.html")


@login_required()
def find_friends(request):
    profiles = request.user.profile.friends.all()
    context = {
        'profiles': profiles,
    }
    return render(request, "accounts/findfriends.html", context)


"""Utilities Functions"""
@login_required()
def pic_save(request, img):
    user_dir = settings.MEDIA_ROOT + "\\" + request.user.username
    dir_creation(request, user_dir)
    user_dir_profile_pics = user_dir + "\\" + 'profile'
    dir_creation(request, user_dir_profile_pics)

    if os.path.isdir(user_dir_profile_pics):
        new_path_of_profile_pics = user_dir_profile_pics + "\\" + img.name
        shutil.move(img.path, new_path_of_profile_pics)
        img = new_path_of_profile_pics
    return img


@login_required()
def dir_creation(request, dir_to_create):
    try:
        os.mkdir(dir_to_create)
    except OSError:
        print("Creation of the directory %s failed" % dir_to_create)
    else:
        print("Successfully created the directory %s " % dir_to_create)
    return