from django.shortcuts import get_object_or_404, redirect, render

from .models import NewsPost


def news_list(request):
    posts = list(NewsPost.objects.filter(is_active=True).order_by("-published_at"))
    featured = posts[0] if posts else None
    other_posts = posts[1:]
    return render(request, "news/news_list.html", {"featured": featured, "posts": other_posts})


def news_detail_by_id(request, pk):
    obj = get_object_or_404(NewsPost, pk=pk, is_active=True)
    return redirect(obj, permanent=True)


def news_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, is_active=True)
    return render(request, "news/news_detail.html", {"post": post})
