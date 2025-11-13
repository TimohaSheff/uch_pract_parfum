from django.shortcuts import render


def index(request):
    """Главная страница"""
    return render(request, 'shop/index.html')


def catalog(request):
    """Страница каталога"""
    return render(request, 'shop/catalog.html')


def contacts(request):
    """Страница контактов"""
    return render(request, 'shop/contacts.html')

