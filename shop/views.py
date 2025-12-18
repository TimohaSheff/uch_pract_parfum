from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.db import transaction
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, LoginForm
from .models import (
    CustomUser, Product, Brand, Category, 
    Cart, CartItem, Order, OrderItem, Review, Wishlist
)


def index(request):
    """Главная страница"""
    # Получаем популярные парфюмы для главной страницы
    featured_products = Product.objects.filter(
        in_stock=True, 
        is_bestseller=True
    )[:6]
    
    new_products = Product.objects.filter(
        in_stock=True,
        is_new=True
    )[:6]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
    }
    return render(request, 'shop/index.html', context)


def catalog(request):
    """Страница каталога парфюмерии с сортировкой и фильтрацией"""
    # Получаем только парфюмы в наличии
    products = Product.objects.filter(in_stock=True)
    
    # Фильтрация по категории (Люкс/Ниша)
    category_id = request.GET.get('category', '')
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            products = products.filter(category=category)
        except (Category.DoesNotExist, ValueError):
            pass
    
    # Фильтрация по концентрации
    concentration = request.GET.get('concentration', '')
    if concentration:
        products = products.filter(concentration=concentration)
    
    # Фильтрация по полу
    gender = request.GET.get('gender', '')
    if gender:
        products = products.filter(gender=gender)
    
    # Фильтрация по бренду
    brand_id = request.GET.get('brand', '')
    if brand_id:
        try:
            brand = Brand.objects.get(id=brand_id)
            products = products.filter(brand=brand)
        except (Brand.DoesNotExist, ValueError):
            pass
    
    # Фильтрация по нотам
    notes = request.GET.get('notes', '')
    if notes:
        if notes == 'woody':
            products = products.filter(
                Q(notes_top__icontains='древ') | 
                Q(notes_middle__icontains='древ') | 
                Q(notes_base__icontains='древ')
            )
        elif notes == 'floral':
            products = products.filter(
                Q(notes_top__icontains='цвет') | 
                Q(notes_middle__icontains='цвет') | 
                Q(notes_base__icontains='цвет')
            )
        elif notes == 'fresh':
            products = products.filter(
                Q(notes_top__icontains='свеж') | 
                Q(notes_middle__icontains='свеж') | 
                Q(notes_base__icontains='свеж')
            )
        elif notes == 'oriental':
            products = products.filter(
                Q(notes_top__icontains='вост') | 
                Q(notes_middle__icontains='вост') | 
                Q(notes_base__icontains='вост')
            )
        elif notes == 'citrus':
            products = products.filter(
                Q(notes_top__icontains='цитрус') | 
                Q(notes_middle__icontains='цитрус') | 
                Q(notes_base__icontains='цитрус')
            )
    
    # Фильтрация по цене
    price_range = request.GET.get('price_range', '')
    if price_range:
        if price_range == '0-5000':
            products = products.filter(price__lte=5000)
        elif price_range == '5000-15000':
            products = products.filter(price__gte=5000, price__lte=15000)
        elif price_range == '15000-30000':
            products = products.filter(price__gte=15000, price__lte=30000)
        elif price_range == '30000+':
            products = products.filter(price__gte=30000)
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    
    if sort_by == 'year':
        # По году (используем год создания записи)
        products = products.order_by('-created_at')
    elif sort_by == 'name':
        # По наименованию (А-Я)
        products = products.order_by('name')
    elif sort_by == 'price':
        # По цене (по возрастанию)
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        # По цене (по убыванию)
        products = products.order_by('-price')
    elif sort_by == 'brand':
        # По бренду
        products = products.order_by('brand__name')
    else:  # newest (по умолчанию) или popular
        if sort_by == 'popular':
            # По популярности (хиты продаж)
            products = products.order_by('-is_bestseller', '-created_at')
        else:
            # По новизне (дата добавления)
            products = products.order_by('-created_at')
    
    # Получаем все данные для фильтров
    categories = Category.objects.all().order_by('name')
    brands = Brand.objects.all().order_by('name')
    
    # Для фильтра концентрации
    CONCENTRATION_CHOICES = Product.CONCENTRATION_CHOICES if hasattr(Product, 'CONCENTRATION_CHOICES') else []
    
    context = {
        'products': products,
        'categories': categories,  # QuerySet объектов Category
        'concentration_choices': CONCENTRATION_CHOICES,  # Для фильтра концентрации
        'brands': brands,
        'current_category': category_id,
        'current_concentration': concentration,
        'current_gender': gender,
        'current_brand': brand_id,
        'current_notes': notes,
        'current_price_range': price_range,
        'current_sort': sort_by,
    }
    
    return render(request, 'shop/catalog.html', context)


def product_detail(request, slug):
    """Страница парфюма"""
    try:
        product = Product.objects.get(slug=slug, in_stock=True)
    except Product.DoesNotExist:
        raise Http404("Парфюм не найден или нет в наличии")
    
    # Похожие парфюмы (той же категории или бренда)
    similar_products = Product.objects.filter(
        in_stock=True
    ).exclude(id=product.id).filter(
        Q(category=product.category) | Q(brand=product.brand)
    )[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    
    return render(request, 'shop/product_detail.html', context)


def contacts(request):
    """Страница контактов"""
    return render(request, 'shop/contacts.html')


@ensure_csrf_cookie
def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'shop/register.html')


@ensure_csrf_cookie
def login_view(request):
    """Страница авторизации"""
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'shop/login.html')


@require_http_methods(["POST"])
@csrf_exempt
def register_api(request):
    """API для регистрации с AJAX валидацией"""
    if request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Вы уже авторизованы'})
    
    try:
        data = json.loads(request.body)
        # Преобразуем rules из строки в boolean
        if 'rules' in data:
            data['rules'] = data['rules'] == True or data['rules'] == 'true' or data['rules'] == 'True'
        
        form = RegistrationForm(data)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Регистрация успешна!',
                'redirect': '/'
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] if error_list else ''
            return JsonResponse({
                'success': False,
                'errors': errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["POST"])
@csrf_exempt
def login_api(request):
    """API для авторизации с AJAX валидацией"""
    if request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Вы уже авторизованы'})
    
    try:
        data = json.loads(request.body)
        form = LoginForm(data)
        
        if form.is_valid():
            login_value = form.cleaned_data['login']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=login_value, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Авторизация успешна!',
                    'redirect': '/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': {'__all__': 'Неверный логин или пароль'}
                })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] if error_list else ''
            return JsonResponse({
                'success': False,
                'errors': errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('index')


def about(request):
    """Страница о компании"""
    return render(request, 'shop/about.html')


def search(request):
    """Поиск парфюмов"""
    query = request.GET.get('q', '').strip()
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(description__icontains=query) |
            Q(notes_top__icontains=query) |
            Q(notes_middle__icontains=query) |
            Q(notes_base__icontains=query),
            in_stock=True
        ).order_by('-created_at')
    
    context = {
        'query': query,
        'products': products,
        'results_count': len(products),
    }
    
    return render(request, 'shop/search.html', context)


def brands(request):
    """Страница с брендами"""
    brands_list = Brand.objects.all().order_by('name')
    
    # Считаем товары каждого бренда
    for brand in brands_list:
        brand.product_count = Product.objects.filter(
            brand=brand, 
            in_stock=True
        ).count()
    
    context = {
        'brands': brands_list,
    }
    
    return render(request, 'shop/brands.html', context)


def brand_detail(request, slug):
    """Страница конкретного бренда"""
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand, in_stock=True)
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest (по умолчанию)
        products = products.order_by('-created_at')
    
    context = {
        'brand': brand,
        'products': products,
        'current_sort': sort_by,
    }
    
    return render(request, 'shop/brand_detail.html', context)


def category_detail(request, slug):
    """Страница конкретной категории (Люкс/Ниша)"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, in_stock=True)
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest (по умолчанию)
        products = products.order_by('-created_at')
    
    context = {
        'category': category,
        'products': products,
        'current_sort': sort_by,
    }
    
    return render(request, 'shop/category_detail.html', context)

from django.contrib import messages
from django.db import transaction

@login_required
def cart_view(request):
    """Страница корзины"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'shop/cart.html', context)


@require_http_methods(["POST"])
@csrf_exempt
@login_required
def add_to_cart_api(request, product_id):
    """API для добавления товара в корзину"""
    try:
        product = Product.objects.get(id=product_id, in_stock=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            message = 'Количество увеличено'
        else:
            message = 'Товар добавлен в корзину'
        
        cart.save()  # Обновляем дату изменения корзины
        
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total': cart.get_total_items(),
            'item_total': cart_item.get_total_price(),
            'cart_total_price': cart.get_total_price()
        })
        
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Товар не найден или нет в наличии'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["POST"])
@csrf_exempt
@login_required
@require_http_methods(["POST"])
@csrf_exempt
@login_required
def update_cart_item_api(request, item_id):
    """API для обновления количества товара в корзине"""
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({
                'success': False,
                'error': 'Количество должно быть положительным'
            })
        
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        
        # ЗАМЕНЯЕМ лимит с 10 на 100
        if quantity > 100:  # Новый лимит 100 штук
            return JsonResponse({
                'success': False,
                'error': 'Максимальное количество - 100'
            })
        
        cart_item.quantity = quantity
        cart_item.save()
        
        cart = cart_item.cart
        cart.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Количество обновлено',
            'item_total': cart_item.get_total_price(),
            'cart_total_price': cart.get_total_price(),
            'cart_total': cart.get_total_items()
        })
        
    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Товар не найден в корзине'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["POST"])
@csrf_exempt
@login_required
def remove_from_cart_api(request, item_id):
    """API для удаления товара из корзины"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        cart.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Товар удален из корзины',
            'cart_total_price': cart.get_total_price(),
            'cart_total': cart.get_total_items()
        })
        
    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Товар не найден в корзине'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def checkout_view(request):
    """Страница оформления заказа"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    
    if not items.exists():
        return redirect('cart')
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'shop/checkout.html', context)


@require_http_methods(["POST"])
@csrf_exempt
@login_required
def create_order_api(request):
    """API для создания заказа с проверкой пароля"""
    try:
        print("=== ORDER CREATION STARTED ===")  # Для отладки
        data = json.loads(request.body)
        print("Request data:", data)  # Для отладки
        
        password = data.get('password', '')
        
        # Проверка пароля
        if not request.user.check_password(password):
            print("Password check FAILED")  # Для отладки
            return JsonResponse({
                'success': False,
                'error': 'Неверный пароль'
            })
        
        print("Password check PASSED")  # Для отладки
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.select_related('product').all()
        
        if not items.exists():
            return JsonResponse({
                'success': False,
                'error': 'Корзина пуста'
            })
        
        # Проверяем наличие всех товаров
        for item in items:
            if not item.product.in_stock:
                return JsonResponse({
                    'success': False,
                    'error': f'Товар "{item.product.name}" отсутствует на складе'
                })
        
        # Создаем заказ
        with transaction.atomic():
            # Генерируем номер заказа
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=f'ORD-{date_str}').order_by('-id').first()
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            order_number = f'ORD-{date_str}-{new_num:04d}'
            
            # Получаем данные из запроса
            address = data.get('address', 'Не указан')
            city = data.get('city', 'Не указан')
            postal_code = data.get('postal_code', '')
            comment = data.get('comment', '')
            payment_method = data.get('payment_method', 'cash')  # По умолчанию наличные
            
            print(f"Creating order with payment method: {payment_method}")  # Для отладки
            
            order = Order.objects.create(
                order_number=order_number,
                user=request.user,
                status='pending',
                payment_method=payment_method,  # Используем переданный метод оплаты
                total_price=cart.get_total_price(),
                full_name=f"{request.user.surname} {request.user.name} {request.user.patronymic or ''}".strip(),
                email=request.user.email,
                phone=request.user.phone_number or '',
                address=address,
                city=city,
                postal_code=postal_code,
                comment=comment
            )
            
            # Создаем элементы заказа
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    product_price=item.product.get_discounted_price(),
                    quantity=item.quantity
                )
            
            # Очищаем корзину
            cart.items.all().delete()
            cart.save()
        
        print(f"Order created successfully: {order_number}")  # Для отладки
        
        return JsonResponse({
            'success': True,
            'message': 'Заказ успешно создан!',
            'order_number': order.order_number,
            'redirect': '/'  # URL для страницы после оформления
        })
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")  # Для отладки
        return JsonResponse({
            'success': False,
            'error': 'Ошибка формата данных'
        })
    except Exception as e:
        print(f"Order creation error: {e}")  # Для отладки
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@require_http_methods(["POST"])
@csrf_exempt
@login_required
def add_to_cart_api(request, product_id):
    """API для добавления товара в корзину"""
    try:
        product = Product.objects.get(id=product_id, in_stock=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            message = 'Количество увеличено'
        else:
            message = 'Товар добавлен в корзину'
        
        cart.save()  # Обновляем дату изменения корзины
        
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total': cart.get_total_items(),
            'item_total': cart_item.get_total_price(),
            'cart_total_price': cart.get_total_price()
        })
        
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Товар не найден или нет в наличии'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
    
@login_required
def account_view(request):
    """Страница личного кабинета"""
    # Получаем заказы пользователя от новых к старым
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items')
    
    # Считаем общее количество товаров во всех заказах
    total_items = sum(order.items.count() for order in orders)
    
    context = {
        'orders': orders,
        'total_items': total_items,
    }
    
    return render(request, 'shop/account.html', context)


@csrf_exempt
@require_POST
def delete_order_api(request, order_id):
    """API для удаления заказа через AJAX"""
    try:
        # Проверяем авторизацию пользователя
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Требуется авторизация'}, status=401)
        
        # Получаем заказ
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Проверяем, можно ли удалить заказ
        if order.status == 'pending':
            order.delete()
            return JsonResponse({
                'success': True, 
                'message': 'Заказ успешно удален',
                'order_id': order_id
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Нельзя удалить заказ с текущим статусом'
            }, status=400)
            
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Заказ не найден'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f'Ошибка при удалении: {str(e)}'
        }, status=500)
    
@login_required
def delete_order(request, order_id):
    """Удаление заказа через обычную форму (не API)"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Проверяем, можно ли удалить заказ
        if order.status == 'pending':
            order.delete()
            messages.success(request, f'Заказ №{order.order_number} успешно удален')
        else:
            messages.error(request, 'Нельзя удалить заказ с текущим статусом')
            
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден')
    
    return redirect('account')

@login_required
def cancel_order(request, order_id):
    """Отмена заказа (меняет статус на 'cancelled')"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Проверяем, можно ли отменить заказ
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Заказ №{order.order_number} отменен')
        else:
            messages.error(request, 'Нельзя отменить заказ с текущим статусом')
            
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден')
    
    return redirect('account')

@login_required
def order_detail(request, order_id):
    """Детали заказа"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        items = order.items.all()
        
        context = {
            'order': order,
            'items': items,
            'title': f'Заказ №{order.order_number}',
        }
        
        return render(request, 'shop/order_detail.html', context)
        
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден')
        return redirect('account')
    
def about_view(request):
    """Страница "О компании" """
    context = {
        'title': 'О компании',
        'description': 'Информация о нашей компании'
    }
    return render(request, 'shop/about.html', context)

