from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

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


class CustomPasswordResetForm(forms.Form):
    """
    فرم درخواست بازیابی رمز عبور — فقط ایمیل می‌گیرد.
    عمداً هیچ خطایی برای «ایمیل پیدا نشد» نشان نمی‌دهیم (نه اینجا، نه در
    view)، چون این کار می‌تواند لو بدهد کدام ایمیل‌ها در سایت ثبت‌نام
    کرده‌اند؛ فقط فرمت ایمیل را اعتبارسنجی می‌کنیم.
    """
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Enter your email',
        })
    )


class CustomSetPasswordForm(forms.Form):
    """
    فرم تنظیم رمز عبور جدید بعد از کلیک روی لینک بازیابی.
    کاملاً دستی نوشته شده (نه ارث‌بری از SetPasswordForm آماده‌ی جنگو):
    - چک می‌کند دو فیلد رمز عبور با هم یکسان باشند
    - رمز عبور را از طریق validate_password در برابر AUTH_PASSWORD_VALIDATORS
      پروژه اعتبارسنجی می‌کند (همان قوانینی که برای ثبت‌نام هم اعمال می‌شود)
    """
    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'common-input mb-20 form-control',
            'placeholder': 'New password',
        })
    )
    new_password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Confirm new password',
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password and self.user is not None:
            try:
                validate_password(password, self.user)
            except DjangoValidationError as exc:
                raise forms.ValidationError(list(exc.messages))
        return password

    def clean_new_password2(self):
        p1 = self.cleaned_data.get('new_password1')
        p2 = self.cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('دو فیلد رمز عبور با هم مطابقت ندارند.')
        return p2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user
