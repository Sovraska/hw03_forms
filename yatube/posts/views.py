from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import PostForm
from .models import Group, Post, User

PAGE_LIMIT = 10


def pagination(request, post_list):
    paginator = Paginator(post_list, PAGE_LIMIT)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    template = 'posts/index.html'

    post_list = Post.objects.select_related("group")

    page_obj = pagination(request=request, post_list=post_list)

    context = {
        'page_obj': page_obj,
    }

    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'

    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()

    page_obj = pagination(request=request, post_list=post_list)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'

    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()

    page_obj = pagination(request=request, post_list=post_list)
    #иначе авто тесты на сайте не проходит ему нужно в username передавать автора
    context = {
        'post_list': post_list,
        'user': user,
        'username': user, 
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)

    posts = Post.objects.filter(author=post.author)

    context = {
        'posts': posts,
        'post': post,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return HttpResponseRedirect(reverse("posts:profile",
                                                args=[request.user, ]))

    context = {
        'form': form,
        "form_errors": form.errors,
        'is_edit': False}

    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    posts = Post.objects.select_related('group')
    post = get_object_or_404(posts, id=post_id)
    form = PostForm()
    if post.author != request.user:
        return HttpResponseRedirect(reverse('posts:index'))

    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('posts:post_detail',
                                                args=[post_id, ]))

    return render(request, template, {'form': form, 'is_edit': True})
