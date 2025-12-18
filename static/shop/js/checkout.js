// checkout.js - ВСЕ ФУНКЦИИ ДОЛЖНЫ БЫТЬ В ГЛОБАЛЬНОЙ ОБЛАСТИ ВИДИМОСТИ

// Глобальные переменные
let isSubmitting = false;

// Функция показа ошибки - ДОЛЖНА БЫТЬ ГЛОБАЛЬНОЙ
function showError(message) {
    console.error('Showing error:', message);
    
    // Показываем в alert для надежности
    alert('ОШИБКА: ' + message);
    
    // Также показываем в div если есть
    const errorDiv = document.getElementById('password-error');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.style.color = '#c62828';
        errorDiv.style.fontSize = '12px';
        errorDiv.style.marginTop = '8px';
        errorDiv.style.padding = '10px';
        errorDiv.style.backgroundColor = '#ffebee';
        errorDiv.style.border = '1px solid #ffcdd2';
        
        // Автоматическое скрытие через 10 секунд
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 10000);
    }
}

// Получение CSRF токена - ДОЛЖНА БЫТЬ ГЛОБАЛЬНОЙ
function getCsrfToken() {
    // Пытаемся получить из cookie
    const name = 'csrftoken';
    let cookieValue = null;
    
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    
    // Если не нашли в куках, ищем в скрытом поле
    if (!cookieValue) {
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) {
            cookieValue = csrfInput.value;
        }
    }
    
    // Если не нашли, ищем в мета-тегах
    if (!cookieValue) {
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        if (csrfMeta) {
            cookieValue = csrfMeta.getAttribute('content');
        }
    }
    
    console.log('CSRF token found:', cookieValue ? 'YES' : 'NO');
    return cookieValue;
}

// ОСНОВНАЯ ФУНКЦИЯ ОФОРМЛЕНИЯ ЗАКАЗА - ДОЛЖНА БЫТЬ ГЛОБАЛЬНОЙ
function submitOrder() {
    console.log('=== submitOrder() called ===');
    
    if (isSubmitting) {
        console.log('Already submitting, ignoring click');
        return;
    }
    
    isSubmitting = true;
    
    // Собираем данные формы
    const password = document.getElementById('password');
    const address = document.getElementById('address');
    const city = document.getElementById('city');
    const postalCode = document.getElementById('postal_code');
    const comment = document.getElementById('comment');
    
    if (!password || !address || !city) {
        console.error('Form elements not found!');
        showError('Ошибка загрузки формы. Пожалуйста, обновите страницу.');
        isSubmitting = false;
        return;
    }
    
    const passwordValue = password.value.trim();
    const addressValue = address.value.trim();
    const cityValue = city.value.trim();
    const postalCodeValue = postalCode ? postalCode.value.trim() : '';
    const commentValue = comment ? comment.value.trim() : '';
    
    // Получаем выбранный способ оплаты
    const paymentMethodRadio = document.querySelector('input[name="payment_method"]:checked');
    if (!paymentMethodRadio) {
        showError('Выберите способ оплаты');
        isSubmitting = false;
        return;
    }
    const paymentMethod = paymentMethodRadio.value;
    
    console.log('Form data:', {
        password: passwordValue ? '***' : 'empty',
        address: addressValue,
        city: cityValue,
        postal_code: postalCodeValue,
        comment: commentValue,
        payment_method: paymentMethod
    });
    
    // Валидация
    if (!passwordValue) {
        showError('Введите пароль для подтверждения');
        password.focus();
        isSubmitting = false;
        return;
    }
    
    if (!addressValue) {
        showError('Введите адрес доставки');
        address.focus();
        isSubmitting = false;
        return;
    }
    
    if (!cityValue) {
        showError('Введите город доставки');
        city.focus();
        isSubmitting = false;
        return;
    }
    
    // Получаем CSRF токен
    const csrfToken = getCsrfToken();
    if (!csrfToken) {
        showError('Ошибка безопасности. Обновите страницу и попробуйте снова.');
        isSubmitting = false;
        return;
    }
    
    console.log('CSRF token found');
    
    // Подготавливаем данные для отправки
    const orderData = {
        password: passwordValue,
        address: addressValue,
        city: cityValue,
        postal_code: postalCodeValue,
        comment: commentValue,
        payment_method: paymentMethod
    };
    
    console.log('Sending order data:', orderData);
    
    // Показываем индикатор загрузки
    const submitBtn = document.querySelector('.submit-order-btn');
    if (!submitBtn) {
        console.error('Submit button disappeared!');
        isSubmitting = false;
        return;
    }
    
    const originalText = submitBtn.textContent;
    const originalBgColor = submitBtn.style.backgroundColor;
    
    submitBtn.textContent = 'ОБРАБОТКА...';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';
    submitBtn.style.backgroundColor = '#666';
    
    // Отправляем запрос
    fetch('/api/order/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(orderData)
    })
    .then(response => {
        console.log('Response status:', response.status, response.statusText);
        
        if (response.status === 403) {
            throw new Error('Ошибка авторизации. Возможно, сессия истекла.');
        }
        
        if (response.status === 400) {
            return response.json().then(data => {
                throw new Error(data.error || 'Неверный запрос');
            });
        }
        
        if (!response.ok) {
            throw new Error(`HTTP ошибка: ${response.status}`);
        }
        
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        
        if (data.success) {
            // Успешное оформление
            console.log('Order created successfully:', data.order_number);
            
            // Показываем успешное сообщение
            submitBtn.textContent = 'УСПЕШНО!';
            submitBtn.style.backgroundColor = '#27ae60';
            
            setTimeout(() => {
                alert(`ЗАКАЗ УСПЕШНО ОФОРМЛЕН!\n\nНомер вашего заказа: ${data.order_number}\n\nС вами свяжется менеджер для подтверждения.`);
                window.location.href = data.redirect || '/';
            }, 500);
            
        } else {
            // Ошибка от сервера
            console.error('Server error:', data.error);
            showError(data.error || 'Неизвестная ошибка сервера');
            
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.backgroundColor = originalBgColor;
            isSubmitting = false;
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        
        let errorMessage = 'Ошибка сети или сервера. ';
        
        if (error.message.includes('NetworkError')) {
            errorMessage += 'Проверьте подключение к интернету.';
        } else if (error.message.includes('Failed to fetch')) {
            errorMessage += 'Сервер не отвечает.';
        } else {
            errorMessage += error.message;
        }
        
        showError(errorMessage);
        
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        submitBtn.style.backgroundColor = originalBgColor;
        isSubmitting = false;
    });
}

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log('Checkout page loaded');
    
    // Инициализация выбора способа оплаты
    document.querySelectorAll('.payment-option').forEach(option => {
        option.addEventListener('click', function() {
            console.log('Payment option clicked:', this.querySelector('input').value);
            document.querySelectorAll('.payment-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            this.classList.add('selected');
            this.querySelector('input').checked = true;
        });
    });
    
    // Добавляем обработчик на кнопку (если еще нет onclick в HTML)
    const submitBtn = document.querySelector('.submit-order-btn');
    if (submitBtn && !submitBtn.onclick) {
        console.log('Adding event listener to submit button');
        submitBtn.addEventListener('click', submitOrder);
    } else if (submitBtn && submitBtn.onclick) {
        console.log('Button already has onclick handler');
    } else {
        console.error('Submit button NOT found!');
    }
    
    // Убираем старый onclick из HTML если есть
    if (submitBtn) {
        submitBtn.removeAttribute('onclick');
    }
    
    // Тестовая функция (только для разработки)
    window.testOrder = function() {
        console.log('=== TEST ORDER ===');
        
        // Заполняем форму тестовыми данными
        document.getElementById('password').value = 'admin123'; // Используй реальный пароль пользователя
        document.getElementById('address').value = 'Тестовый адрес, д. 1';
        document.getElementById('city').value = 'Москва';
        document.getElementById('postal_code').value = '123456';
        document.getElementById('comment').value = 'Тестовый заказ';
        
        // Выбираем способ оплаты
        const firstOption = document.querySelector('.payment-option');
        if (firstOption) {
            firstOption.click();
        }
        
        console.log('Form filled with test data');
        console.log('Run submitOrder() to test');
    };
});