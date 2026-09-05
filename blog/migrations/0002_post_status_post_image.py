from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.BooleanField(default=False, help_text='اگر فعال باشد یعنی ادمین اجازه‌ی انتشار این پست را داده است.'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='تصویر شاخص این پست.', null=True, upload_to='blog/'),
        ),
    ]
