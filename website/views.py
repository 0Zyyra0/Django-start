from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .forms import TicketForm, SignUpForm, EmailOrUsernameLoginForm


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