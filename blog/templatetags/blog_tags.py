from django import template
from django.utils import timezone

from blog.models import Post, Category

register = template.Library()


@register.inclusion_tag('blog/tags/latest_posts.html')
def latest_posts(count=6):
    """
    آخرین N پست منتشرشده را برمی‌گرداند.
    پست مجاز پستی است که هم status=True باشد و هم published_date آن گذشته باشد.
    استفاده در تمپلیت: {% load blog_tags %}  ...  {% latest_posts %}  یا  {% latest_posts 6 %}
    """
    posts = Post.objects.filter(
        status=True,
        published_date__lte=timezone.now(),
    ).order_by('-published_date')[:count]

    return {'posts': posts}


@register.inclusion_tag('blog/tags/category_list.html')
def category_list():
    """
    لیست دسته‌بندی‌ها به همراه تعداد پست منتشرشده‌ی هرکدام.
    استفاده در تمپلیت: {% load blog_tags %}  ...  {% category_list %}
    """
    now = timezone.now()
    categories = Category.objects.all()

    data = [
        {
            'category': category,
            'count': category.posts.filter(status=True, published_date__lte=now).count(),
        }
        for category in categories
    ]

    return {'categories': data}
