from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    cyrillic_validator = RegexValidator(
        regex=r'^[А-Яа-яЁё\s\-]+$',
        message='Разрешены только кириллица, пробел и тире'
    )
    
    latin_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\-]+$',
        message='Разрешены только латиница, цифры и тире'
    )
    
    name = forms.CharField(
        label='Имя',
        max_length=100,
        required=True,
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя'
        })
    )
    
    surname = forms.CharField(
        label='Фамилия',
        max_length=100,
        required=True,
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите фамилию'
        })
    )
    
    patronymic = forms.CharField(
        label='Отчество',
        max_length=100,
        required=False,
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите отчество (необязательно)'
        })
    )
    
    login = forms.CharField(
        label='Логин',
        max_length=50,
        required=True,
        validators=[latin_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    
    password = forms.CharField(
        label='Пароль',
        min_length=6,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль (минимум 6 символов)'
        })
    )
    
    password_repeat = forms.CharField(
        label='Повторите пароль',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )
    
    rules = forms.BooleanField(
        label='Я согласен с правилами регистрации',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'patronymic', 'login', 'email', 'password']
    
    def clean_login(self):
        login = self.cleaned_data.get('login')
        if CustomUser.objects.filter(login=login).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return login
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean_password_repeat(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password and password_repeat and password != password_repeat:
            raise ValidationError('Пароли не совпадают')
        return password_repeat
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Логин',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин'
        })
    )
    
    password = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

