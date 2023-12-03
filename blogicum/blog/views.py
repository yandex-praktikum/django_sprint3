from django.shortcuts import render
from django.http import Http404


def index(request):
    template = 'blog/index.html'
    context = {'posts': posts[::-1]}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    try:
        post = posts[int(id)]
    except IndexError:
        raise Http404("Пост не найден")  # Возбуждение ошибки 404
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    context = {'category_slug': category_slug}
    return render(request, template, context)
