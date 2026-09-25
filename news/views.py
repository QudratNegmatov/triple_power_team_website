from django.shortcuts import get_object_or_404, render

from .models import NewsPost


def news_list(request):
    posts = NewsPost.objects.filter(is_active=True)
    return render(request, "news/news_list.html", {"posts": posts})


def news_detail(request, pk):
    post = get_object_or_404(NewsPost, pk=pk, is_active=True)
    return render(request, "news/news_detail.html", {"post": post})
