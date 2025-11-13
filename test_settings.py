#!/usr/bin/env python
"""Тестовый скрипт для проверки настроек"""
import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

# Устанавливаем settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'perfume_shop.settings'

try:
    import django
    django.setup()
    
    from django.conf import settings
    print(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")
    print(f"INSTALLED_APPS: {settings.INSTALLED_APPS}")
    print(f"Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    # Проверяем URL-маршруты
    from django.urls import get_resolver
    resolver = get_resolver()
    print(f"\nURL patterns found: {len(resolver.url_patterns)}")
    for pattern in resolver.url_patterns:
        print(f"  - {pattern.pattern}")
        
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()

