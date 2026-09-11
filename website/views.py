from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import (
    TicketForm,
    SignUpForm,
    EmailOrUsernameLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from .models import NewsletterSubscriber
from .tokens import generate_reset_token, verify_reset_token


def index_view(request):
    return render(request, 'website/index.html')


def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)

            # فارغ از اینکه کاربر توی فیلد نام چه چیزی وارد کرده،
            # همیشه مقدار نام را «ناشناس» قرار می‌دهیم (قدرت برتری روی ورودی کاربر)
            ticket.name = 'ناشناس'

            ticket.save()

            messages.success(request, 'پیام شما با موفقیت ثبت شد. متشکریم!')
            return redirect('contact')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید.')
    else:
        form = TicketForm()

    return render(request, 'website/contact.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='website.backends.EmailOrUsernameModelBackend')
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد. خوش آمدید!')
            return redirect('index')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید.')
    else:
        form = SignUpForm()

    return render(request, 'website/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = EmailOrUsernameLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # این خط با بک‌اند سفارشی EmailOrUsernameModelBackend کار می‌کند
            # و identifier می‌تواند هم username باشد و هم email
            user = authenticate(request, username=identifier, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'خوش آمدید {user.username}!')
                next_url = request.GET.get('next') or 'index'
                return redirect(next_url)
            else:
                messages.error(request, 'نام کاربری/ایمیل یا رمز عبور اشتباه است.')
    else:
        form = EmailOrUsernameLoginForm()

    return render(request, 'website/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('index')


def password_reset_view(request):
    """
    مرحله‌ی اول بازیابی رمز عبور (سفارشی): کاربر ایمیلش را وارد می‌کند.
    اگر کاربری با آن ایمیل پیدا شود، یک لینک ریست (شامل uid و توکن
    سفارشی) برایش ایمیل می‌شود. برای اینکه نشود فهمید چه ایمیل‌هایی در
    سایت ثبت‌نام کرده‌اند، در هر دو حالت (پیدا شد/نشد) کاربر به همان صفحه‌ی
    «لینک ارسال شد» هدایت می‌شود.
    """
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email__iexact=email, is_active=True)

            for user in users:
                # کاربری که رمز قابل استفاده ندارد (مثلاً فقط با گوگل وارد می‌شود)
                # نباید بتواند رمز عبور «تنظیم» کند از این مسیر
                if not user.has_usable_password():
                    continue

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = generate_reset_token(user)
                reset_path = reverse(
                    'password_reset_confirm',
                    kwargs={'uidb64': uid, 'token': token},
                )
                reset_url = request.build_absolute_uri(reset_path)

                subject = render_to_string(
                    'website/password_reset_subject.txt', {}
                ).strip().replace('\n', ' ')
                message = render_to_string('website/password_reset_email.html', {
                    'user': user,
                    'protocol': request.scheme,
                    'domain': request.get_host(),
                    'uid': uid,
                    'token': token,
                })

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'website/password_reset.html', {'form': form})


def password_reset_done_view(request):
    return render(request, 'website/password_reset_done.html')


def password_reset_confirm_view(request, uidb64, token):
    """
    مرحله‌ی دوم بازیابی رمز عبور (سفارشی): کاربر از روی لینک ایمیل
    به اینجا می‌آید. uidb64 را باز می‌کنیم تا کاربر را پیدا کنیم و
    توکن را با verify_reset_token (منطق دستی خودمان) اعتبارسنجی می‌کنیم.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    validlink = user is not None and verify_reset_token(user, token)

    form = None
    if validlink:
        if request.method == 'POST':
            form = CustomSetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد.')
                return redirect('password_reset_complete')
        else:
            form = CustomSetPasswordForm(user=user)

    return render(request, 'website/password_reset_confirm.html', {
        'form': form,
        'validlink': validlink,
    })


def password_reset_complete_view(request):
    return render(request, 'website/password_reset_complete.html')


def newsletter_signup_view(request):
    """
    فرم خبرنامه‌ای که در فوتر همه‌ی صفحات هست. قبلاً به یک آدرس Mailchimp
    متعلق به سازنده‌ی اصلی تمپلیت اشاره می‌کرد؛ الان ایمیل واقعاً در
    دیتابیس خودمان ذخیره می‌شود.
    """
    if request.method == 'POST':
        email = request.POST.get('EMAIL', '').strip()
        try:
            validate_email(email)
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, 'با موفقیت در خبرنامه عضو شدید!')
        except ValidationError:
            messages.error(request, 'ایمیل وارد شده معتبر نیست.')

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer or 'index')