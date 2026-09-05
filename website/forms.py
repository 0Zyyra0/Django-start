from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'common-input mb-20 form-control',
                'placeholder': 'Enter your name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'common-input mb-20 form-control',
                'placeholder': 'Enter email address',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'common-input mb-20 form-control',
                'placeholder': 'Enter subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'common-textarea form-control',
                'placeholder': 'Enter Message',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # مقدار subject الزامی نیست، هم توی فرم و هم توی دیتابیس می‌تواند خالی ذخیره شود
        self.fields['subject'].required = False


class SignUpForm(UserCreationForm):
    """
    فرم ثبت‌نام گسترش‌یافته: علاوه بر username و password، فیلد email هم
    اجباری و یکتاست تا بعداً بشود با همان ایمیل هم وارد شد.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Enter email address',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Enter username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Enter password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Confirm password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('کاربری با این ایمیل قبلاً ثبت‌نام کرده است.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EmailOrUsernameLoginForm(forms.Form):
    """
    فرم ورود: به‌جای دو فیلد جدا برای نام کاربری و ایمیل، فقط یک فیلد
    گرفته می‌شود و در view هم با username و هم با email کاربر مطابقت داده می‌شود.
    """
    username = forms.CharField(
        label='نام کاربری یا ایمیل',
        widget=forms.TextInput(attrs={
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Username or Email',
        })
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Password',
        })
    )
