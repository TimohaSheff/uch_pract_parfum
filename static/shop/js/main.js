    // Slider functionality
    let currentSlideIndex = 0;
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');

    function showSlide(index) {
        // Hide all slides
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        // Show current slide
        if (index >= slides.length) {
            currentSlideIndex = 0;
        } else if (index < 0) {
            currentSlideIndex = slides.length - 1;
        } else {
            currentSlideIndex = index;
        }
        
        slides[currentSlideIndex].classList.add('active');
        dots[currentSlideIndex].classList.add('active');
    }

    function changeSlide(direction) {
        showSlide(currentSlideIndex + direction);
    }

    function currentSlide(index) {
        showSlide(index - 1);
    }

    // Auto-play slider
    let slideInterval = setInterval(() => {
        changeSlide(1);
    }, 5000);

    // Pause on hover
    const slider = document.getElementById('slider');
    if (slider) {
        slider.addEventListener('mouseenter', () => {
            clearInterval(slideInterval);
        });
        
        slider.addEventListener('mouseleave', () => {
            slideInterval = setInterval(() => {
                changeSlide(1);
            }, 5000);
        });
    }

    // Initialize slider
    document.addEventListener('DOMContentLoaded', () => {
        showSlide(0);
    });

    function addToCart(productId) {
        console.log('Добавляем товар ID:', productId);
        
        fetch(`/api/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // ТОЛЬКО обновляем счетчик, без уведомлений
                if (data.cart_total !== undefined) {
                    updateCartCounter(data.cart_total);
                }
            } else {
                // Без alert, только в консоль
                console.error('Ошибка добавления:', data.error);
            }
        })
        .catch(error => {
            console.error('Ошибка сети:', error);
        });
    }

    function updateCartCounter(count) {
        let counter = document.querySelector('.cart-counter');
        if (!counter) {
            // Создаем если нет
            counter = document.createElement('span');
            counter.className = 'cart-counter';
            // Добавляем в шапку рядом с иконкой корзины
            const cartIcon = document.querySelector('.header-cart');
            if (cartIcon) {
                cartIcon.appendChild(counter);
            }
        }
        
        counter.textContent = count;
        if (count > 0) {
            counter.style.display = 'inline-block';
        } else {
            counter.style.display = 'none';
        }
    }

    // Получаем CSRF токен из cookie
    function getCsrfToken() {
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
        return cookieValue;
    }

    // Показ уведомлений
    function showNotification(message, type = 'info') {
        // Создаем элемент уведомления
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Добавляем в тело документа
        document.body.appendChild(notification);
        
        // Автоматическое удаление через 5 секунд
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // При загрузке страницы обновляем счетчик корзины
    document.addEventListener('DOMContentLoaded', function() {
        // Проверяем авторизацию по наличию cookie
        const isAuthenticated = document.cookie.includes('sessionid');
        
        if (isAuthenticated) {
            // Просто устанавливаем начальное значение 0, 
            // реальное значение обновится при взаимодействии с корзиной
            updateCartCounter(0);
            
            // Или можно добавить отдельный эндпоинт для получения количества
            // fetch('/api/cart/count/')
            //     .then(response => response.json())
            //     .then(data => {
            //         if (data.success) {
            //             updateCartCounter(data.count);
            //         }
            //     });
        }
    });

    // Добавьте эти стили для уведомлений в ваш CSS
    const notificationStyles = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 8px;
            padding: 16px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-width: 300px;
            max-width: 400px;
            z-index: 9999;
            animation: slideIn 0.3s ease-out;
            border-left: 4px solid #4CAF50;
        }
        
        .notification-error {
            border-left-color: #f44336;
        }
        
        .notification-info {
            border-left-color: #2196F3;
        }
        
        .notification-content {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .notification-content i {
            font-size: 20px;
            color: #4CAF50;
        }
        
        .notification-error .notification-content i {
            color: #f44336;
        }
        
        .notification-info .notification-content i {
            color: #2196F3;
        }
        
        .notification-close {
            background: none;
            border: none;
            color: #999;
            cursor: pointer;
            padding: 4px;
            margin-left: 10px;
            font-size: 16px;
        }
        
        .notification-close:hover {
            color: #333;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;

    // Добавляем стили для уведомлений
    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = notificationStyles;
    document.head.appendChild(styleSheet);

    // Функции для работы с корзиной
function updateQuantity(itemId, change) {
    const input = document.querySelector(`[data-item-id="${itemId}"] .qty-input`);
    let newValue = parseInt(input.value) + change;
    
    if (newValue < 1) newValue = 1;
    if (newValue > 100) newValue = 100;
    
    input.value = newValue;
    updateCartItem(itemId, newValue);
}

function updateQuantityInput(itemId, value) {
    let newValue = parseInt(value);
    
    if (isNaN(newValue) || newValue < 1) newValue = 1;
    if (newValue > 100) newValue = 100;
    
    const input = document.querySelector(`[data-item-id="${itemId}"] .qty-input`);
    input.value = newValue;
    
    updateCartItem(itemId, newValue);
}

function updateCartItem(itemId, quantity) {
    fetch(`/api/cart/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Обновляем отображение суммы для товара
            const totalElement = document.querySelector(`[data-item-id="${itemId}"] .total-price`);
            if (totalElement) {
                totalElement.textContent = data.item_total + ' ₽';
            }
            
            // Обновляем сводку
            updateCartSummary(data);
            
            // Обновляем счетчик в шапке
            updateCartCounter(data.cart_total);
        }
    })
    .catch(error => {
        console.error('Error updating cart:', error);
    });
}

function removeFromCart(itemId) {
    if (!confirm('Удалить товар из корзины?')) return;
    
    fetch(`/api/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Удаляем строку из таблицы с анимацией
            const itemRow = document.querySelector(`[data-item-id="${itemId}"]`);
            if (itemRow) {
                itemRow.style.opacity = '0';
                itemRow.style.transform = 'translateX(-20px)';
                
                setTimeout(() => {
                    itemRow.remove();
                    
                    // Обновляем сводку
                    updateCartSummary(data);
                    
                    // Обновляем счетчик в шапке
                    updateCartCounter(data.cart_total);
                    
                    // Если корзина пуста, перезагружаем страницу
                    if (data.cart_total === 0) {
                        setTimeout(() => {
                            window.location.reload();
                        }, 300);
                    }
                }, 300);
            }
        }
    })
    .catch(error => {
        console.error('Error removing from cart:', error);
    });
}

function updateCartSummary(data) {
    const itemsCount = document.getElementById('items-count');
    const subtotal = document.getElementById('subtotal');
    const totalPrice = document.getElementById('total-price');
    
    if (itemsCount) itemsCount.textContent = data.cart_total + ' шт.';
    if (subtotal) subtotal.textContent = data.cart_total_price + ' ₽';
    if (totalPrice) totalPrice.textContent = data.cart_total_price + ' ₽';
}

function updateCartCounter(count) {
    const counter = document.querySelector('.cart-counter');
    if (counter) {
        counter.textContent = count;
        counter.style.display = count > 0 ? 'flex' : 'none';
        
        // Анимация обновления
        counter.classList.add('updated');
        setTimeout(() => counter.classList.remove('updated'), 300);
    }
}

function getCsrfToken() {
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
    return cookieValue;
}

// Добавление меток для мобильных устройств
document.addEventListener('DOMContentLoaded', function() {
    if (window.innerWidth <= 768) {
        const productCols = document.querySelectorAll('.col-product');
        const priceCols = document.querySelectorAll('.col-price');
        const quantityCols = document.querySelectorAll('.col-quantity');
        const totalCols = document.querySelectorAll('.col-total');
        
        productCols.forEach(col => col.setAttribute('data-label', 'Товар'));
        priceCols.forEach(col => col.setAttribute('data-label', 'Цена'));
        quantityCols.forEach(col => col.setAttribute('data-label', 'Кол-во'));
        totalCols.forEach(col => col.setAttribute('data-label', 'Сумма'));
    }
});