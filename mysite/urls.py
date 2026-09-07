"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from mysite.sitemaps import PostSitemap, CategorySitemap, StaticViewSitemap

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'pages': StaticViewSitemap,
}


if getattr(settings, 'MAINTENANCE_MODE', False):
    # قبل از راه‌اندازی نهایی سایت: تمام درخواست‌ها (هر آدرسی که باشد)
    # به صفحه‌ی "به‌زودی در دسترس خواهد بود" هدایت می‌شوند.
    # فقط پنل ادمین در دسترس می‌ماند تا بتوان بعداً MAINTENANCE_MODE را غیرفعال کرد.
    urlpatterns = [
        path('admin/', admin.site.urls),
        re_path(r'^.*$', TemplateView.as_view(template_name='coming_soon.html')),
    ]
else:
    urlpatterns = [
        path('admin/', admin.site.urls),
        # path ( 'url address' , ' view ' )
        path('', include('website.urls')),
        path('blog/', include('blog.urls')),

        # سئو: نقشه‌ی سایت و robots.txt
        path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
        path(
            'robots.txt',
            TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
            name='robots_txt',
        ),
    ]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)