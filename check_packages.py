#!/usr/bin/env python
"""Скрипт для проверки установленных пакетов"""
import subprocess
import sys

# Проверяем установленные пакеты
result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                       capture_output=True, text=True)

print("Установленные пакеты, содержащие 'perfumery' или 'perfume':")
for line in result.stdout.split('\n'):
    if 'perfumery' in line.lower() or 'perfume' in line.lower():
        print(f"  {line}")

