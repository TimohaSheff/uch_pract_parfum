# Команды Git для загрузки проекта

Выполните следующие команды в Git Bash:

## 1. Инициализация репозитория
```bash
git init
```

## 2. Первый коммит - создание структуры проекта
```bash
git add requirements.txt
git add manage.py
git add perfume_shop/
git add .gitignore
git add README.md
git commit -m "Создание структуры Django проекта и requirements.txt"
```

## 3. Второй коммит - создание приложения shop
```bash
git add shop/
git commit -m "Создание приложения shop с базовыми настройками"
```

## 4. Третий коммит - создание шаблонов и навигации
```bash
git add shop/templates/
git commit -m "Создание базового шаблона с навигацией (логотип, название, ссылки, кнопки авторизации)"
```

## 5. Четвертый коммит - создание страниц
```bash
git add shop/templates/shop/index.html
git add shop/templates/shop/catalog.html
git add shop/templates/shop/contacts.html
git commit -m "Создание страниц: Главная (с девизом и слайдером), Каталог, Контакты"
```

## 6. Пятый коммит - стили и JavaScript
```bash
git add static/
git commit -m "Добавление CSS стилей и JavaScript для слайдера"
```

## 7. Настройка удаленного репозитория (если нужно)
```bash
git remote add origin <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
git branch -M main
git push -u origin main
```

## Альтернативный вариант - все файлы одним коммитом
Если хотите сделать все сразу:
```bash
git init
git add .
git commit -m "Создание интернет-магазина парфюмерии на Django"
```

