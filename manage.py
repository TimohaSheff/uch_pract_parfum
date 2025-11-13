#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# КРИТИЧЕСКИ ВАЖНО: Устанавливаем settings модуль ДО импорта Django
# Это должно быть сделано до любого импорта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')
# Принудительно переопределяем, если был установлен другой
os.environ['DJANGO_SETTINGS_MODULE'] = 'perfume_shop.settings'

def main():
    """Run administrative tasks."""
    # Убеждаемся, что settings модуль установлен правильно
    if os.environ.get('DJANGO_SETTINGS_MODULE') != 'perfume_shop.settings':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'perfume_shop.settings'
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

