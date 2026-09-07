# Travel & Adventure — پروژه‌ی پایانی دوره‌ی جنگو

یک وب‌سایت کامل بلاگ/معرفی که تقریباً تمام مباحث تدریس‌شده در دوره را در بر می‌گیرد.

## بخش‌های اصلی سایت

- **صفحه‌ی اصلی (Home):** معرفی سایت + آخرین پست‌های بلاگ (با template tag سفارشی)
- **درباره‌ی ما (About)**
- **تماس با ما (Contact):** فرم واقعی متصل به دیتابیس
- **بلاگ:** لیست پست‌ها، صفحه‌ی تکی هر پست (با پست قبلی/بعدی)، صفحه‌ی هر دسته‌بندی، و جست‌وجو
- **احراز هویت:** ثبت‌نام، ورود (با نام کاربری یا ایمیل)، خروج، فراموشی رمز عبور

## ویژگی‌ها و ماژول‌های استفاده‌شده

| بخش | توضیح |
|---|---|
| مدل‌ها | `Post`, `Category` (اپ blog) و `Ticket`, `NewsletterSubscriber` (اپ website) |
| پنل ادمین | سفارشی‌سازی‌شده برای همه‌ی مدل‌ها (`list_display`, `list_filter`, `search_fields`, `list_editable`) |
| فرم‌ها | `ModelForm` برای تماس، `UserCreationForm` گسترش‌یافته برای ثبت‌نام، فرم سفارشی ورود |
| احراز هویت سفارشی | بک‌اند اختصاصی برای ورود با نام کاربری **یا** ایمیل |
| فراموشی رمز عبور | با توابع آماده‌ی `django.contrib.auth` |
| Template Tags سفارشی | `latest_posts`, `category_list` (اپ blog) |
| پیام‌های سیستم (Messages) | پاپ‌آپ مشترک در `base.html` که در همه‌ی صفحات نمایش داده می‌شود |
| سئو | عنوان و توضیحات داینامیک هر صفحه، `sitemap.xml` (با `django.contrib.sitemaps`)، `robots.txt`، `noindex` روی صفحات کاربری |
| فشرده‌سازی Assets | `django-compressor` برای ادغام و فشرده‌سازی CSS/JS |
| حالت تعمیر/راه‌اندازی | `MAINTENANCE_MODE` در تنظیمات، با catch-all در `urls.py` |
| صفحات خطای سفارشی | `404.html`, `500.html` |
| آماده برای هاست | تنظیمات از طریق متغیر محیطی، `.htaccess` برای یکسان‌سازی دامنه و HTTPS |

## اجرای محلی (Local Development)

```bash
python -m venv venv
venv\Scripts\activate        # ویندوز
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## راهنمای انتشار روی هاست (Production Deployment)

این پروژه برای هاست‌های اشتراکی مبتنی بر **Apache + Passenger/mod_wsgi** (رایج در هاست‌های ایرانی) آماده شده است.

### ۱. متغیرهای محیطی
قبل از اجرا روی هاست، این متغیرها را در پنل هاست (یا فایل `.env` بسته به نوع هاست) تنظیم کنید:

```
DJANGO_SECRET_KEY=<یک کلید تصادفی و طولانی جدید>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=domain.ir,www.domain.ir
```

⚠️ **هرگز** پروژه را با `DJANGO_DEBUG=True` روی هاست واقعی اجرا نکنید.

### ۲. نصب و آماده‌سازی
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### ۳. فایل `.htaccess`
فایل `.htaccess` موجود در ریشه‌ی پروژه، آدرس‌های `www.domain.ir` و نسخه‌ی HTTP را به `https://domain.ir` هدایت می‌کند. قبل از آپلود، مقدار `domain.ir` داخل این فایل را با دامنه‌ی واقعی خودتان جایگزین کنید.

### ۴. قبل از باز کردن سایت به‌روی کاربران
اگر سایت هنوز کامل آماده نیست، در `settings.py` مقدار زیر را موقتاً `True` بگذارید تا صفحه‌ی «به‌زودی در دسترس خواهد بود» نمایش داده شود:
```python
MAINTENANCE_MODE = True
```
بعد از آماده شدن کامل سایت، آن را به `False` برگردانید.

### ۵. بررسی نهایی قبل از انتشار
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` تغییر کرده و مخفی نگه داشته شده
- [ ] `ALLOWED_HOSTS` شامل دامنه‌ی واقعی است
- [ ] `MAINTENANCE_MODE = False`
- [ ] `python manage.py collectstatic` اجرا شده
- [ ] گواهی SSL روی هاست فعال است
- [ ] `EMAIL_BACKEND` برای ارسال واقعی ایمیل (مثلاً SMTP) تنظیم شده — در حال حاضر روی حالت توسعه (چاپ در کنسول) است
