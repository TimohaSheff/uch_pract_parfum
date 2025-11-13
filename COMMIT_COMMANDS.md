# Команды для коммита изменений

Выполните следующие команды в Git Bash:

## 1. Проверка статуса
```bash
git status
```

## 2. Добавление файлов
```bash
git add shop/models.py
git add shop/forms.py
git add shop/views.py
git add shop/admin.py
git add shop/urls.py
git add shop/templates/shop/register.html
git add shop/templates/shop/login.html
git add shop/templates/shop/base.html
git add static/shop/css/style.css
git add static/shop/js/auth.js
git add perfume_shop/settings.py
```

## 3. Коммиты по этапам

### Коммит 1: Создание модели пользователя
```bash
git add shop/models.py shop/admin.py perfume_shop/settings.py
git commit -m "Создание модели CustomUser с полями name, surname, patronymic, login, email, password"
```

### Коммит 2: Создание форм регистрации и авторизации
```bash
git add shop/forms.py
git commit -m "Создание форм RegistrationForm и LoginForm с валидацией всех полей"
```

### Коммит 3: Создание views для обработки форм
```bash
git add shop/views.py shop/urls.py
git commit -m "Создание views для регистрации, авторизации и API endpoints с AJAX валидацией"
```

### Коммит 4: Создание шаблонов форм
```bash
git add shop/templates/shop/register.html shop/templates/shop/login.html shop/templates/shop/base.html
git commit -m "Создание шаблонов для форм регистрации и авторизации"
```

### Коммит 5: Добавление JavaScript и стилей
```bash
git add static/shop/js/auth.js static/shop/css/style.css
git commit -m "Добавление AJAX валидации без перезагрузки страницы и стилей для форм"
```

## Альтернативный вариант - один коммит
```bash
git add .
git commit -m "Реализация форм регистрации и авторизации с AJAX валидацией

- Создана модель CustomUser с валидацией полей
- Формы регистрации и авторизации с полной валидацией
- AJAX валидация без перезагрузки страницы
- Обновлена навигация с ссылками на формы"
```

