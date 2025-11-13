#!/usr/bin/env python
"""Диагностический скрипт для проверки проблемы с settings"""
import os
import sys

print("=== Диагностика проблемы с Django settings ===\n")

# 1. Проверяем переменную окружения
print("1. Переменная окружения DJANGO_SETTINGS_MODULE:")
print(f"   {os.environ.get('DJANGO_SETTINGS_MODULE', 'НЕ УСТАНОВЛЕНА')}\n")

# 2. Устанавливаем правильный settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'perfume_shop.settings'
print("2. Установлен DJANGO_SETTINGS_MODULE = 'perfume_shop.settings'\n")

# 3. Проверяем, можем ли импортировать settings
try:
    import django
    django.setup()
    from django.conf import settings
    print("3. Django settings загружены:")
    print(f"   ROOT_URLCONF: {settings.ROOT_URLCONF}")
    print(f"   INSTALLED_APPS: {settings.INSTALLED_APPS[:3]}...")
    print(f"   Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}\n")
except Exception as e:
    print(f"3. Ошибка при загрузке settings: {e}\n")

# 4. Проверяем, есть ли perfumery_project в sys.modules
print("4. Проверка sys.modules на наличие perfumery_project:")
perfumery_modules = [m for m in sys.modules.keys() if 'perfumery' in m.lower()]
if perfumery_modules:
    print(f"   Найдены модули: {perfumery_modules}")
else:
    print("   Модули perfumery_project не найдены\n")

# 5. Проверяем путь Python
print("5. Python path:")
for p in sys.path[:5]:
    print(f"   {p}")

