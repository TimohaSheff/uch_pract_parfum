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