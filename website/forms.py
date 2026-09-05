from django import forms

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
