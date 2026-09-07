from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from blog.models import Post, Category


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=True, published_date__lte=timezone.now())

    def lastmod(self, obj):
        return obj.published_date

    def location(self, obj):
        return reverse('blog:single', args=[obj.pk])


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('blog:category', args=[obj.slug])


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return ['index', 'about', 'contact', 'blog:index']

    def location(self, item):
        return reverse(item)
