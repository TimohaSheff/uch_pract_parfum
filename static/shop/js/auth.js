// Функция для получения CSRF токена
function getCookie(name) {
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

// Функция для очистки ошибок
function clearErrors() {
    document.querySelectorAll('.error-message').forEach(el => {
        el.textContent = '';
    });
    document.querySelectorAll('.form-control').forEach(el => {
        el.classList.remove('error');
    });
    const messagesDiv = document.getElementById('form-messages');
    if (messagesDiv) {
        messagesDiv.style.display = 'none';
        messagesDiv.className = 'form-messages';
    }
}

// Функция для отображения ошибок
function showErrors(errors) {
    clearErrors();
    
    for (const [field, message] of Object.entries(errors)) {
        if (field === '__all__') {
            const messagesDiv = document.getElementById('form-messages');
            if (messagesDiv) {
                messagesDiv.textContent = message;
                messagesDiv.className = 'form-messages error';
                messagesDiv.style.display = 'block';
            }
        } else {
            const errorElement = document.getElementById(`error_${field}`);
            const inputElement = document.getElementById(`id_${field}`);
            
            if (errorElement) {
                errorElement.textContent = message;
            }
            if (inputElement) {
                inputElement.classList.add('error');
            }
        }
    }
}

// Функция для отображения успешного сообщения
function showSuccess(message) {
    clearErrors();
    const messagesDiv = document.getElementById('form-messages');
    if (messagesDiv) {
        messagesDiv.textContent = message;
        messagesDiv.className = 'form-messages success';
        messagesDiv.style.display = 'block';
    }
}

// Обработка формы регистрации
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(registerForm);
        const data = {};
        formData.forEach((value, key) => {
            if (key === 'rules') {
                data[key] = registerForm.querySelector('#id_rules').checked;
            } else {
                data[key] = value;
            }
        });
        
        try {
            const response = await fetch('/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showSuccess(result.message);
                setTimeout(() => {
                    window.location.href = result.redirect || '/';
                }, 1500);
            } else {
                if (result.errors) {
                    showErrors(result.errors);
                } else if (result.error) {
                    showErrors({ '__all__': result.error });
                }
            }
        } catch (error) {
            showErrors({ '__all__': 'Произошла ошибка при отправке формы' });
        }
    });
}

// Обработка формы авторизации
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(loginForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        try {
            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showSuccess(result.message);
                setTimeout(() => {
                    window.location.href = result.redirect || '/';
                }, 1500);
            } else {
                if (result.errors) {
                    showErrors(result.errors);
                } else if (result.error) {
                    showErrors({ '__all__': result.error });
                }
            }
        } catch (error) {
            showErrors({ '__all__': 'Произошла ошибка при отправке формы' });
        }
    });
}

// Валидация в реальном времени
document.addEventListener('DOMContentLoaded', function() {
    const forms = [registerForm, loginForm].filter(f => f !== null);
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                const fieldName = this.name;
                const errorElement = document.getElementById(`error_${fieldName}`);
                
                if (errorElement && errorElement.textContent) {
                    // Ошибка уже отображается, не очищаем
                    return;
                }
                
                // Простая валидация на клиенте
                if (this.hasAttribute('required') && !this.value.trim()) {
                    if (errorElement) {
                        errorElement.textContent = 'Это поле обязательно для заполнения';
                        this.classList.add('error');
                    }
                } else {
                    if (errorElement) {
                        errorElement.textContent = '';
                        this.classList.remove('error');
                    }
                }
            });
        });
    });
});

