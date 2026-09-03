from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post


def blog_view(request):
    # فقط پست‌هایی که زمان published_date آن‌ها از الان گذشته باشد نمایش داده شوند
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'blog/blog-home.html', {'posts': posts})


def blog_single(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # هر بار که این view فراخوانی شود، یک واحد به تعداد بازدید اضافه می‌شود
    post.counted_view += 1
    post.save(update_fields=['counted_view'])

    recent_posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).exclude(pk=post.pk)[:4]

    return render(request, 'blog/blog-single.html', {
        'post': post,
        'recent_posts': recent_posts,
    })