import json
import os
import shutil
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Image, TopicOfPost
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (TemplateView,
                                  DetailView, CreateView, UpdateView, DeleteView)
from accounts.models import Profile
from django.conf import settings


class AboutView(TemplateView):
    """View shows about page"""
    template_name = 'about.html'


def PostList(request):
    """View shows all posts"""
    if request.user.is_authenticated:
        users = Profile.objects.exclude(user=request.user)
    else:
        users = Profile.objects.all()
    posts = Post.objects.all().order_by('-created_date')

    topics = topics_info_to_json()

    context = {
        'users': users,
        'posts': posts,
        'friends_label': 'Make Friends',
        'topics': topics,
    }
    return render(request, "blog/post_list.html", context)


class PostDetailView(DetailView):
    """View shows post details"""
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        images = Image.objects.filter(post=self.object)
        context = {'post': self.object, 'images': images}
        return render(request, 'blog/post_detail.html', context)


class CreatePostView(LoginRequiredMixin, CreateView):
    """View creates new post"""
    template_name = 'blog/post_form.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        """If method is POST"""
        form = PostForm(request.POST)
        images = request.FILES.getlist('image_field')
        form.instance.author = self.request.user
        if form.is_valid():
            form.save()
            topic_of_post = get_object_or_404(TopicOfPost, topic=form.instance.topic)
            topic_of_post.count += 1
            topic_of_post.save()
            if images:
                for image in images:
                    img = Image.objects.create(post=form.instance, image=image)
                    pic_save(self.request, img, form.instance.title)
            return redirect('post_detail', pk=form.instance.pk)
        return render(request, 'blog/post_form.html', {'form': PostForm})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View updates post details"""
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        """If method is POST"""
        form = PostForm(request.POST)
        images = request.FILES.getlist('image_field')
        post = self.get_object()
        if form.is_valid():
            post.title = form.instance.title
            post.text = form.instance.text
            post.save()
            if images:
                for image in images:
                    img = Image.objects.create(post=post, image=image)
                    pic_save(self.request, img, post.title)
            return redirect('post_detail', pk=post.pk)
        return render(request, 'blog/post_form.html', {'form': PostForm})

    def test_func(self):
        """Test func, checks conditions"""
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View deletes a post"""
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        """Test func, checks conditions"""
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


##################################################
# Addition functionality to posts
##################################################


def add_comment_to_post(request, pk):
    """Add new comment to post"""
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_remove(request, pk):
    """Remove comment from post"""
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    post = get_object_or_404(Post, pk=post_pk)
    if post.author == request.user:
        comment.delete()
    return redirect('post_detail', pk=post_pk)


@login_required()
def like_to_post(request, pk):
    """Add like to post"""
    post = get_object_or_404(Post, pk=pk)
    if request.user.profile not in post.likes.all():
        post.likes.add(request.user.profile)
    return redirect('post_detail', pk)


@login_required()
def unlike_to_post(request, pk):
    """Remove like from post"""
    post = get_object_or_404(Post, pk=pk)
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
    return redirect('post_detail', pk)

##################################################
# Utilities Functions
##################################################


def topics_info_to_json():
    """Convert python objects to jason format"""
    topics = TopicOfPost.objects.all()
    names_of_topics = []
    counts_of_topics = []
    for topic in topics:
        names_of_topics.append(topic.topic)
        counts_of_topics.append(topic.count)
    json_names_of_topics = json.dumps(names_of_topics)
    json_counts_of_topics = json.dumps(counts_of_topics)
    topics = {'names_of_topics': json_names_of_topics, 'counts_of_topics': json_counts_of_topics}
    return topics


@login_required()
def pic_save(request, img, title):
    """Saves pic of a post"""
    user_dir = settings.MEDIA_ROOT + "\\" + request.user.username
    dir_creation(request, user_dir)
    user_dir_posts_pics = user_dir + "\\" + 'posts'
    dir_creation(request, user_dir_posts_pics)
    post_folders_name = str(title)
    user_dir_posts_pics = user_dir_posts_pics + "\\" + post_folders_name
    dir_creation(request, user_dir_posts_pics)
    if os.path.isdir(user_dir_posts_pics):
        new_path_of_posts_pics = user_dir_posts_pics + "\\" + img.image.name
        shutil.move(img.image.path, new_path_of_posts_pics)
        img.image = new_path_of_posts_pics
        img.save()
    return


@login_required()
def dir_creation(dir_to_create):
    """Creates a new directory"""
    try:
        os.mkdir(dir_to_create)
    except OSError:
        print("Creation of the directory %s failed" % dir_to_create)
    else:
        print("Successfully created the directory %s " % dir_to_create)
    return
