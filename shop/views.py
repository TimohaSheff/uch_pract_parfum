from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json
from .forms import RegistrationForm, LoginForm
from .models import CustomUser


def index(request):
    """Главная страница"""
    return render(request, 'shop/index.html')


def catalog(request):
    """Страница каталога"""
    return render(request, 'shop/catalog.html')


def contacts(request):
    """Страница контактов"""
    return render(request, 'shop/contacts.html')


@ensure_csrf_cookie
def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'shop/register.html')


@ensure_csrf_cookie
def login_view(request):
    """Страница авторизации"""
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'shop/login.html')


@require_http_methods(["POST"])
@csrf_exempt
def register_api(request):
    """API для регистрации с AJAX валидацией"""
    if request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Вы уже авторизованы'})
    
    try:
        data = json.loads(request.body)
        # Преобразуем rules из строки в boolean
        if 'rules' in data:
            data['rules'] = data['rules'] == True or data['rules'] == 'true' or data['rules'] == 'True'
        
        form = RegistrationForm(data)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Регистрация успешна!',
                'redirect': '/'
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] if error_list else ''
            return JsonResponse({
                'success': False,
                'errors': errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["POST"])
@csrf_exempt
def login_api(request):
    """API для авторизации с AJAX валидацией"""
    if request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Вы уже авторизованы'})
    
    try:
        data = json.loads(request.body)
        form = LoginForm(data)
        
        if form.is_valid():
            login_value = form.cleaned_data['login']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=login_value, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Авторизация успешна!',
                    'redirect': '/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': {'__all__': 'Неверный логин или пароль'}
                })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] if error_list else ''
            return JsonResponse({
                'success': False,
                'errors': errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('index')
