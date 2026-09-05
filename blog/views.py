from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category


def blog_view(request):
    # پست مجاز پستی است که هم ادمین انتشارش را فعال کرده باشد (status=True)
    # و هم زمان انتشارش رسیده باشد (published_date <= الان)
    posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
    return render(request, 'blog/blog-home.html', {'posts': posts})


def blog_single(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # هر بار که این view فراخوانی شود، یک واحد به تعداد بازدید اضافه می‌شود
    post.counted_view += 1
    post.save(update_fields=['counted_view'])

    # لیست کلی پست‌های مجاز (status=True و published_date گذشته)، مرتب از قدیم به جدید
    published_posts = list(
        Post.objects.filter(
            status=True, published_date__lte=timezone.now()
        ).order_by('published_date')
    )

    previous_post = None
    next_post = None

    if post in published_posts:
        current_index = published_posts.index(post)

        # اگر آیتمی قبل از ایندکس فعلی وجود داشته باشد
        if current_index > 0:
            previous_post = published_posts[current_index - 1]

        # اگر آیتمی بعد از ایندکس فعلی وجود داشته باشد
        if current_index < len(published_posts) - 1:
            next_post = published_posts[current_index + 1]

    recent_posts = [p for p in published_posts if p.pk != post.pk][:4]

    return render(request, 'blog/blog-single.html', {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'recent_posts': recent_posts,
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)

    # همان فیلتر استاندارد (status=True و published_date گذشته)، این‌بار فقط برای این دسته‌بندی
    posts = Post.objects.filter(
        status=True,
        published_date__lte=timezone.now(),
        category=category,
    )

    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts,
    })