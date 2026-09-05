
from django.urls import path
from django.contrib.auth import views as auth_views
from website.views import *


urlpatterns = [
    path('', index_view, name='index'),
    path('about', about_view, name='about'),
    path('contact', contact_view, name='contact'),

    # احراز هویت (ثبت‌نام / ورود با نام کاربری یا ایمیل / خروج)
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # فراموشی رمز عبور - با استفاده از توابع آماده‌ی django.contrib.auth
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='website/password_reset.html',
            email_template_name='website/password_reset_email.html',
            subject_template_name='website/password_reset_subject.txt',
            success_url='/password-reset/done/',
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='website/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='website/password_reset_confirm.html',
            success_url='/reset/done/',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='website/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
]