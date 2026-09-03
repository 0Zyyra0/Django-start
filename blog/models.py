from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(
        help_text='زمانی که پست باید منتشر (published) شود.'
    )
    counted_view = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
