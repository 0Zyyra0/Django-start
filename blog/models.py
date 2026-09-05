from django.db import models
from django.utils.text import Truncator
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(
        help_text='زمانی که پست باید منتشر (published) شود.'
    )
    counted_view = models.PositiveIntegerField(default=0)
    status = models.BooleanField(
        default=False,
        help_text='اگر فعال باشد یعنی ادمین اجازه‌ی انتشار این پست را داده است.'
    )
    image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        help_text='تصویر شاخص این پست.'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def excerpt(self):
        # به‌جای بریدن متن بر اساس تعداد کاراکتر (Truncator.chars)،
        # این‌جا بر اساس تعداد کلمه (Truncator.words) خلاصه می‌سازیم
        return Truncator(self.content).words(30, truncate=' ...')
