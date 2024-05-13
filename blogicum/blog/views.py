from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now


from .models import Post, Category


def get_published_posts(category_posts):
    category_posts = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True,
    )
    return category_posts


def index(request):
    post_list = published_post(category_posts)[:settings.POSTS_BY_PAGE]
    return render(
        request, 'blog/index.html', context={'post_list': post_list}
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        published_post(category_posts),
        pk=post_id,
    )
    return render(request, 'blog/detail.html', context={'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True
        )
    )
    post_list = get_published_posts(category_posts).filter(
        category__slug=category_slug
    )
    return render(request, 'blog/category.html',
                  context={'category': category, 'post_list': post_list})
