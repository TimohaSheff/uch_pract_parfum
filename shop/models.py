from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    # Валидаторы
    cyrillic_validator = RegexValidator(
        regex=r'^[А-Яа-яЁё\s\-]+$',
        message='Разрешены только кириллица, пробел и тире'
    )
    
    latin_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\-]+$',
        message='Разрешены только латиница, цифры и тире'
    )
    
    # Обязательные поля
    name = models.CharField(
        'Имя',
        max_length=100,
        validators=[cyrillic_validator]
    )
    
    surname = models.CharField(
        'Фамилия',
        max_length=100,
        validators=[cyrillic_validator]
    )
    
    patronymic = models.CharField(
        'Отчество',
        max_length=100,
        blank=True,
        null=True,
        validators=[cyrillic_validator]
    )
    
    login = models.CharField(
        'Логин',
        max_length=50,
        unique=True,
        validators=[latin_validator]
    )
    
    email = models.EmailField(
        'Email',
        unique=True
    )
    
    phone_number = models.CharField(
        'Номер телефона',
        max_length=20,
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'name', 'surname']
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f'{self.surname} {self.name} ({self.login})'
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser


class Brand(models.Model):
    """Бренд парфюмерии"""
    name = models.CharField('Название бренда', max_length=100, unique=True)
    slug = models.SlugField('URL', max_length=100, unique=True)
    description = models.TextField('Описание бренда', blank=True)
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True, null=True)
    country = models.CharField('Страна происхождения', max_length=100)
    year_founded = models.IntegerField('Год основания', validators=[MinValueValidator(1700)])
    
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    """Категория парфюмерии"""
    name = models.CharField('Название категории', max_length=100, unique=True)
    slug = models.SlugField('URL', max_length=100, unique=True)
    description = models.TextField('Описание категории', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар (парфюм)"""
    
    # Выбор для кого
    GENDER_CHOICES = [
        ('women', 'Женский'),
        ('men', 'Мужской'),
        ('unisex', 'Унисекс'),
    ]
    
    # Концентрация парфюма (бывшие "категории")
    CONCENTRATION_CHOICES = [
        ('perfume', 'Парфюмерная вода (Eau de Parfum)'),
        ('toilette', 'Туалетная вода (Eau de Toilette)'),
        ('cologne', 'Одеколон (Eau de Cologne)'),
        ('extrait', 'Экстракт (Extrait de Parfum)'),
        ('body', 'Парфюмированное масло/лосьон'),
    ]
    
    # Основные поля
    name = models.CharField('Название парфюма', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name='Бренд',
        related_name='products'
    )
    
    # Категория (Люкс/Ниша) и целевая аудитория
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True,
        related_name='products'
    )
    gender = models.CharField(
        'Для кого',
        max_length=10,
        choices=GENDER_CHOICES,
        default='unisex'
    )
    concentration = models.CharField(
        'Концентрация',
        max_length=20,
        choices=CONCENTRATION_CHOICES,
        default='perfume'
    )
    
    # Цена и скидки
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    discount = models.IntegerField(
        'Скидка (%)',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Объем
    volume = models.IntegerField(
        'Объем (мл)',
        validators=[MinValueValidator(1)]
    )
    
    # Описание и ноты
    description = models.TextField('Описание парфюма')
    notes_top = models.CharField('Верхние ноты', max_length=200, blank=True)
    notes_middle = models.CharField('Ноты сердца', max_length=200, blank=True)
    notes_base = models.CharField('Базовые ноты', max_length=200, blank=True)
    notes_short = models.CharField(
        'Краткое описание нот',
        max_length=100,
        blank=True,
        help_text='Для отображения в каталоге'
    )
    
    # Изображения
    image = models.ImageField('Основное изображение', upload_to='products/')
    image_secondary = models.ImageField(
        'Дополнительное изображение',
        upload_to='products/',
        blank=True,
        null=True
    )
    
    # Статусы
    is_new = models.BooleanField('Новинка', default=False)
    is_bestseller = models.BooleanField('Хит продаж', default=False)
    is_limited = models.BooleanField('Лимитированная серия', default=False)
    in_stock = models.BooleanField('В наличии', default=True)
    
    # Технические поля
    country = models.CharField('Страна производства', max_length=100)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Парфюм'
        verbose_name_plural = 'Парфюмы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['brand']),
            models.Index(fields=['category']),
            models.Index(fields=['gender']),
        ]
    
    def __str__(self):
        return f"{self.brand.name} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    
    def get_discounted_price(self):
        """Рассчитать цену со скидкой"""
        if self.discount:
            return self.price * (100 - self.discount) / 100
        return self.price
    
    def get_category_display_name(self):
        """Получить отображаемое название категории"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_gender_display_name(self):
        """Получить отображаемое название пола"""
        return dict(self.GENDER_CHOICES).get(self.gender, self.gender)


class Review(models.Model):
    """Отзыв о товаре"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='reviews'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews'
    )
    rating = models.IntegerField(
        'Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField('Текст отзыва')
    advantages = models.TextField('Достоинства', blank=True)
    disadvantages = models.TextField('Недостатки', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # Один отзыв от пользователя на товар
    
    def __str__(self):
        return f"Отзыв от {self.user} на {self.product.name}"


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f"Корзина пользователя {self.user}"
    
    def get_total_price(self):
        """Получить общую стоимость товаров в корзине"""
        return sum(item.get_total_price() for item in self.items.all() if item.product)
    
    def get_total_items(self):
        """Получить общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name='Корзина',
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        default=1,
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity}) в корзине {self.cart.user}"
    
    def get_total_price(self):
        """Получить общую стоимость этого элемента"""
        return self.product.get_discounted_price() * self.quantity
    
    def can_increase(self):
        """Можно ли увеличить количество (проверка наличия)"""
        # Здесь можно добавить логику проверки наличия на складе
        return self.product.in_stock

class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    PAYMENT_CHOICES = [
        ('card', 'Карта онлайн'),
        ('cash', 'Наличными при получении'),
        ('transfer', 'Банковский перевод'),
    ]
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='orders'
    )
    order_number = models.CharField('Номер заказа', max_length=20, unique=True)
    status = models.CharField(
        'Статус заказа',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=20,
        choices=PAYMENT_CHOICES
    )
    total_price = models.DecimalField(
        'Общая стоимость',
        max_digits=10,
        decimal_places=2
    )
    
    # Данные доставки
    full_name = models.CharField('ФИО получателя', max_length=300)
    email = models.EmailField('Email для связи')
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес доставки')
    city = models.CharField('Город', max_length=100)
    postal_code = models.CharField('Почтовый индекс', max_length=20)
    
    # Комментарии
    comment = models.TextField('Комментарий к заказу', blank=True)
    
    created_at = models.DateTimeField('Дата создания заказа', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ №{self.order_number} от {self.user}"
    
    def save(self, *args, **kwargs):
        """Генерация номера заказа при создании"""
        if not self.order_number:
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=f'ORD-{date_str}').order_by('-id').first()
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.order_number = f'ORD-{date_str}-{new_num:04d}'
        super().save(*args, **kwargs)
    
    @property
    def total_items(self):
        """Общее количество товаров в заказе"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def can_be_deleted(self):
        """Можно ли удалить заказ"""
        return self.status == 'pending'
    
    def can_be_deleted(self):
        """Можно ли удалить заказ (только если он в обработке)"""
        return self.status == 'pending'
    
    def can_be_cancelled(self):
        """Можно ли отменить заказ"""
        return self.status in ['pending', 'confirmed']


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Товар'
    )
    product_name = models.CharField('Название товара (на момент заказа)', max_length=200)
    product_price = models.DecimalField(
        'Цена товара (на момент заказа)',
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField('Количество')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity} в заказе {self.order.order_number}"
    
    def get_total_price(self):
        """Получить общую стоимость этого элемента"""
        return self.product_price * self.quantity


class Wishlist(models.Model):
    """Список желаний"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='wishlist'
    )
    products = models.ManyToManyField(
        Product,
        verbose_name='Товары',
        related_name='wishlisted_by',
        blank=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Список желаний'
        verbose_name_plural = 'Списки желаний'
    
    def __str__(self):
        return f"Список желаний пользователя {self.user}"