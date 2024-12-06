from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
import re

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='ایمیل معتبر وارد کنید',
        label='ایمیل',
        error_messages={
            'invalid': 'لطفاً یک آدرس ایمیل معتبر وارد کنید.'
        }
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'نام کاربری'
        self.fields['username'].help_text = 'حداکثر 150 کاراکتر. فقط حروف، اعداد و علامت‌های @ . + - _'
        self.fields['username'].validators = [
            RegexValidator(
                regex='^[a-zA-Z0-9@.+-_]+$',
                message='نام کاربری فقط می‌تواند شامل حروف، اعداد و علامت‌های @ . + - _ باشد',
                code='invalid_username'
            ),
            MinLengthValidator(3, 'نام کاربری باید حداقل 3 کاراکتر باشد')
        ]
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password1'].help_text = 'رمز عبور باید حداقل 8 کاراکتر باشد و شامل حداقل یک حرف بزرگ و یک نماد باشد'
        self.fields['password2'].label = 'تکرار رمز عبور'
        self.fields['password2'].help_text = 'رمز عبور را دوباره وارد کنید'

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            if len(password1) < 8:
                raise forms.ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')
            if not re.search('[A-Z]', password1):
                raise forms.ValidationError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد')
            if not re.search('[!@#$%^&*(),.?":{}|<>]', password1):
                raise forms.ValidationError('رمز عبور باید حداقل یک نماد داشته باشد')
        return password1

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است')
        return email


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'نام کاربری'
        self.fields['password'].label = 'رمز عبور'
        
    def clean(self):
        cleaned_data = super().clean()
        if self._errors:  # If there are errors
            raise forms.ValidationError(
                'نام کاربری یا رمز عبور اشتباه است. لطفاً دوباره تلاش کنید.'
            )
        return cleaned_data
