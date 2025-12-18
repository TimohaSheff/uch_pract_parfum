// ACCOUNT PAGE FUNCTIONALITY
document.addEventListener('DOMContentLoaded', function() {
    console.log('Account page loaded');
    
    // Tab Switching
    const menuItems = document.querySelectorAll('.menu-item:not(.logout)');
    const tabContents = document.querySelectorAll('.tab-content');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabId = this.dataset.tab;
            
            // Update active menu item
            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding tab
            tabContents.forEach(tab => {
                tab.classList.remove('active');
                if (tab.id === tabId + '-tab') {
                    tab.classList.add('active');
                }
            });
        });
    });
    
    // Order Filtering
    const orderFilter = document.getElementById('order-filter');
    if (orderFilter) {
        orderFilter.addEventListener('change', function() {
            const status = this.value;
            const orderCards = document.querySelectorAll('.order-card');
            
            orderCards.forEach(card => {
                if (status === 'all' || card.dataset.status === status) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
            
            console.log('Filtered orders by status:', status);
        });
    }
    
    // Order Details Toggle
    document.querySelectorAll('.details-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const orderId = this.dataset.orderId;
            const details = document.getElementById('details-' + orderId);
            
            if (details.style.display === 'none' || !details.style.display) {
                details.style.display = 'block';
                this.textContent = 'СКРЫТЬ';
            } else {
                details.style.display = 'none';
                this.textContent = 'ПОДРОБНЕЕ';
            }
            
            // Smooth scroll to details
            if (details.style.display === 'block') {
                details.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    // Order Deletion
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const orderId = this.dataset.orderId;
            const orderCard = this.closest('.order-card');
            const orderNumber = orderCard.querySelector('.order-number .value').textContent;
            
            if (confirm(`Вы уверены, что хотите удалить заказ №${orderNumber}?`)) {
                deleteOrder(orderId, orderCard);
            }
        });
    });
    
    // Profile Edit Mode
    const profileEditBtn = document.querySelector('.profile-edit-btn');
    if (profileEditBtn) {
        profileEditBtn.addEventListener('click', function() {
            const form = document.getElementById('profile-form');
            const inputs = form.querySelectorAll('input');
            const submitBtn = form.querySelector('button[type="submit"]');
            
            if (inputs[0].disabled) {
                // Enable edit mode
                inputs.forEach(input => input.disabled = false);
                submitBtn.disabled = false;
                this.textContent = 'ОТМЕНИТЬ';
                
                // Focus on first input
                inputs[0].focus();
                
                console.log('Profile edit mode enabled');
            } else {
                // Disable edit mode
                inputs.forEach(input => input.disabled = true);
                submitBtn.disabled = true;
                this.textContent = 'РЕДАКТИРОВАТЬ';
                
                console.log('Profile edit mode disabled');
            }
        });
    }
    
    // Profile Form Submission
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Here you would typically send the form data to the server
            // For now, just show a success message
            alert('Изменения профиля сохранены!');
            
            // Disable edit mode after save
            const inputs = this.querySelectorAll('input');
            const submitBtn = this.querySelector('button[type="submit"]');
            const editBtn = document.querySelector('.profile-edit-btn');
            
            inputs.forEach(input => input.disabled = true);
            submitBtn.disabled = true;
            editBtn.textContent = 'РЕДАКТИРОВАТЬ';
            
            console.log('Profile changes submitted');
        });
    }
    
    // Initialize order filtering
    if (orderFilter) {
        orderFilter.dispatchEvent(new Event('change'));
    }
});

// Function to delete an order
function deleteOrder(orderId, orderElement) {
    console.log('Deleting order:', orderId);
    
    // Show loading state
    const deleteBtn = orderElement.querySelector('.delete-btn');
    const originalText = deleteBtn.textContent;
    deleteBtn.textContent = 'УДАЛЕНИЕ...';
    deleteBtn.disabled = true;
    
    // In a real application, you would make an API call here
    // For now, simulate deletion
    setTimeout(() => {
        // Remove the order from DOM
        orderElement.style.opacity = '0';
        orderElement.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            orderElement.remove();
            console.log('Order removed from DOM');
            
            // Update order count
            updateOrderCount();
            
            // Show success message
            showNotification('Заказ успешно удален', 'success');
        }, 300);
    }, 1000);
}

// Function to update order count
function updateOrderCount() {
    const orderCards = document.querySelectorAll('.order-card');
    const statNumber = document.querySelector('.stat-number');
    
    if (statNumber) {
        statNumber.textContent = orderCards.length;
        console.log('Order count updated:', orderCards.length);
    }
}

// Function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    // Add styles if not already added
    if (!document.querySelector('#notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: #000;
                color: #fff;
                padding: 15px 20px;
                border: 1px solid #000;
                z-index: 1000;
                display: flex;
                align-items: center;
                justify-content: space-between;
                min-width: 300px;
                max-width: 400px;
                animation: slideIn 0.3s ease;
            }
            
            .notification-success {
                background: #27ae60;
                border-color: #27ae60;
            }
            
            .notification-error {
                background: #f44336;
                border-color: #f44336;
            }
            
            .notification-content {
                flex: 1;
            }
            
            .notification-close {
                background: none;
                border: none;
                color: #fff;
                font-size: 20px;
                cursor: pointer;
                margin-left: 15px;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
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
            
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(styles);
    }
    
    document.body.appendChild(notification);
    
    // Close button functionality
    notification.querySelector('.notification-close').addEventListener('click', function() {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, 5000);
    
    console.log('Notification shown:', message);
}

// Export functions for debugging
window.accountFunctions = {
    deleteOrder: deleteOrder,
    showNotification: showNotification,
    updateOrderCount: updateOrderCount
};

console.log('Account JS initialized');