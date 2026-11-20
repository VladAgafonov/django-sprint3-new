from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_ON_INDEX = 5


def get_published_posts():
    """Публикации, которые можно показывать на сайте."""
    return Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )


def index(request):
    post_list = get_published_posts().order_by('-pub_date')[:POSTS_ON_INDEX]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(get_published_posts(), pk=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_published_posts().filter(
        category=category
    ).order_by('-pub_date')
    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list},
    )
