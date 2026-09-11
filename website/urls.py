
from django.urls import path
from website.views import *


urlpatterns = [
    path('', index_view, name='index'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),

    # احراز هویت (ثبت‌نام / ورود با نام کاربری یا ایمیل / خروج)
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('newsletter/', newsletter_signup_view, name='newsletter_signup'),

    # فراموشی رمز عبور - پیاده‌سازی کاملاً سفارشی (بدون توابع آماده‌ی
    # django.contrib.auth.views)؛ منطق در website/views.py و
    # website/tokens.py نوشته شده است.
    path('password-reset/', password_reset_view, name='password_reset'),
    path('password-reset/done/', password_reset_done_view, name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        password_reset_confirm_view,
        name='password_reset_confirm',
    ),
    path('reset/done/', password_reset_complete_view, name='password_reset_complete'),
]