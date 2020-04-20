import shutil
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserCreateForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
import os
from django.conf import settings
from blog.models import Post, Image
from mailsystem.models import Conversation
from .models import FriendRequest, Profile


def get_or_none(classmodel, **kwargs):
    """Custom get object or return a none"""
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class SignUp(CreateView):
    """View creates a new user"""
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


@login_required
def profile(request):
    """View of logged in user, shows or updates user info and his profile info"""
    if request.method == 'POST':
        """If method is POST, saves new info of user and his profile"""
        img_profile_previous = request.user.profile.image
        img_theme_previous = request.user.profile.theme_image
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            """If picture was changed then put it to the user's pics directory"""
            if img_profile_previous != request.user.profile.image:
                image = pic_save(request, request.user.profile.image)
                request.user.profile.image = image
                request.user.profile.save()
            if img_theme_previous != request.user.profile.theme_image:
                image = pic_save(request, request.user.profile.theme_image)
                request.user.profile.theme_image = image
                request.user.profile.save()
            return redirect('profile')

    else:
        """If method is GET, shows info of user and his profile"""
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        friends = request.user.profile.friends.all()
        sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
        received_friend_requests = FriendRequest.objects.filter(to_user=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'users': friends,
        'sent_friend_requests': sent_friend_requests,
        'received_friend_requests': received_friend_requests,
    }
    return render(request, 'accounts/profile.html', context)


def profile_watch(request, pk):
    """View of another user"""
    user_watch = get_object_or_404(User, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated and request.POST.get('action') == 'StartChat':
        """Creates or shows conversation"""
        con = get_or_none(Conversation, user1=request.user, user2=user_watch)
        if con:
            pk_conversation = con.pk
        else:
            con = get_or_none(Conversation, user1=user_watch, user2=request.user)
            if con:
                pk_conversation = con.pk
            else:
                con = Conversation.objects.create(user1=request.user, user2=user_watch)
                pk_conversation = con.pk
        return redirect('conversation', pk=pk_conversation)

    """If method is GET """
    profile = user_watch.profile
    button_status = 'none'
    if request.user.is_authenticated:
        if profile not in request.user.profile.friends.all():
            button_status = 'not_friend'
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
    """Send a friend request to a user"""
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=user)
        return redirect('profile_watch', pk)


def cancel_friend_request(request, pk):
    """Cancel a friend request that sent to a user"""
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        frequest = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user).first()
        frequest.__str__()
        frequest.delete()
        return redirect('profile_watch', pk)


@login_required()
def accept_friend_request(request, pk):
    """Accept a friend request from user"""
    from_user = get_object_or_404(User, pk=pk)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    frequest.delete()
    return redirect('profile')


def delete_friend_request(request, pk):
    """Delete a friend request from user"""
    from_user = get_object_or_404(User, pk=pk)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return redirect('profile')


@login_required()
def delete_friend(request, pk):
    """Remove friend from friends list"""
    friend_delete = get_object_or_404(User, pk=pk)
    friend_delete.profile.friends.remove(request.user.profile)
    request.user.profile.friends.remove(friend_delete.profile)
    return redirect('profile_watch', pk)


@login_required()
def friends(request):
    """Shows all friends of a user"""
    profiles = request.user.profile.friends.all()
    context = {
        'profiles': profiles,
    }
    return render(request, "accounts/friends.html", context)


@login_required()
def find_friends(request):
    """Shows users of the web app"""
    profiles = []
    users = Profile.objects.all()
    for user in users:
        if user not in request.user.profile.friends:
            profiles.append(user)
    context = {
        'profiles': profiles,
    }
    return render(request, "accounts/findfriends.html", context)


###################################################
# Utilities Functions
###################################################


@login_required()
def pic_save(request, img):
    """Saves a user's pic of profile or theme"""
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
def dir_creation(dir_to_create):
    """Creates new direcotry"""
    try:
        os.mkdir(dir_to_create)
    except OSError:
        print("Creation of the directory %s failed" % dir_to_create)
    else:
        print("Successfully created the directory %s " % dir_to_create)
    return
