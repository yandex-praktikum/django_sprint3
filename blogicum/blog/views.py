from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import Post
from .models import Category
from datetime import datetime


def get_queryset(query):
    return query.select_related(
        'category',
        'location',
        'author'
    ).filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        pub_date__date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('category')[:5]
    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post_detail = get_object_or_404(
        Post.objects.select_related(
            'location', 'author', 'category'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now()
        ),
        pk=post_id
    )
    context = {'post': post_detail}
    return render(request, template, context)


def category_posts(request, category_slug):
    templates = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)

    posts = get_list_or_404(Post,
                            category__slug=category_slug,
                            is_published=True,
                            category__is_published=True,
                            pub_date__lte=datetime.now()
                            )
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, templates, context)