from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Category, Post
from django.http import Http404
from datetime import datetime


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.order_by('-pub_date').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category,
                                 is_published=True,
                                 slug=category_slug)
    posts_list = get_list_or_404(
        Post.objects.all().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now(),
            category__slug=category_slug))

    return render(
        request,
        'blog/category.html',
        {
            'post_list': posts_list,
            'category': category
        }
    )


def post_detail(request, id):
    try:
        post = Post.objects.get(
            pk=id, is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now())
    except Post.DoesNotExist:
        raise Http404('Страницы не существует.')
    return render(request,
                  'blog/detail.html',
                  {'post': post})
