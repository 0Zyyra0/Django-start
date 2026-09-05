from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from .forms import TicketForm


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