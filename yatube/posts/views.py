from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post

User = get_user_model()
PAGE_LIMIT = 10


def index(request):
    template = 'posts/index.html'
    text = 'Это главная страница проекта Yatube'

    post_list = Post.objects.select_related("group")
    paginator = Paginator(post_list, PAGE_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'text': text,
        'page_obj': page_obj,
    }

    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'

    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date')
    paginator = Paginator(post_list, PAGE_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'

    username = get_object_or_404(User, username=username)
    post_list = username.posts.order_by('-pub_date')
    paginator = Paginator(post_list, PAGE_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'post_count': post_list.count(),
        'username': username,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post_object = Post.objects.get(id=post_id)

    posts = Post.objects.filter(author=post_object.author)

    context = {
        'post_count': posts.count(),
        'post': post_object,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    is_edit = False
    template = 'posts/create_post.html'

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect(f"/profile/{request.user}/")

    form = PostForm()
    return render(request, template, {'form': form, 'is_edit': is_edit})


@login_required
def post_edit(request, post_id):
    is_edit = True
    template = 'posts/create_post.html'

    post_object = Post.objects.get(id=post_id)


    if post_object.author != request.user:
        return redirect('/')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post_object)
        if form.is_valid():
            form.save()
            return redirect(f"/posts/{post_id}")

    form = PostForm()
    return render(request, template, {'form': form, 'is_edit': is_edit})
