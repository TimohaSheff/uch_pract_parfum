from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CustomUser, Brand, Category, Product, 
    Review, Cart, CartItem, Order, OrderItem, Wishlist
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'name', 'surname', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('login', 'email', 'name', 'surname')
    ordering = ('-date_joined',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'year_founded', 'product_count')
    list_filter = ('country',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество товаров'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'brand', 'category_name', 'gender_display', 
        'concentration_display', 'volume', 'price_with_discount', 
        'in_stock', 'is_new', 'is_bestseller'
    )
    list_filter = (
        'brand', 'category', 'gender', 'concentration', 
        'in_stock', 'is_new', 'is_bestseller', 'is_limited', 'country'
    )
    list_editable = ('in_stock', 'is_new', 'is_bestseller')
    search_fields = ('name', 'brand__name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ()
    
    # Поля для отображения в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'brand', 'category', 'gender', 'concentration', 'description')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'discount', 'in_stock')
        }),
        ('Характеристики', {
            'fields': ('volume', 'country')
        }),
        ('Ноты аромата', {
            'fields': ('notes_top', 'notes_middle', 'notes_base', 'notes_short'),
            'classes': ('collapse',)
        }),
        ('Изображения', {
            'fields': ('image', 'image_secondary')
        }),
        ('Статусы', {
            'fields': ('is_new', 'is_bestseller', 'is_limited'),
            'classes': ('collapse',)
        }),
    )
    
    def category_name(self, obj):
        return obj.category.name if obj.category else '-'
    category_name.short_description = 'Категория'
    
    def concentration_display(self, obj):
        return obj.get_concentration_display()
    concentration_display.short_description = 'Концентрация'
    
    def price_with_discount(self, obj):
        if obj.discount > 0:
            discounted_price = obj.get_discounted_price()
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">{}</span><br>'
                '<span style="color: #d32f2f; font-weight: bold;">{} ₽</span>',
                f"{obj.price} ₽",
                f"{discounted_price} ₽"
            )
        return f"{obj.price} ₽"
    price_with_discount.short_description = 'Цена'
    
    def gender_display(self, obj):
        return obj.get_gender_display()
    gender_display.short_description = 'Для кого'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__login', 'text')
    readonly_fields = ('created_at', 'updated_at')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__login', 'user__email')
    inlines = [CartItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Количество товаров'
    
    def total_price(self, obj):
        return f"{obj.get_total_price()} ₽"
    total_price.short_description = 'Общая стоимость'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user', 'status', 'payment_method', 
        'total_price', 'city', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'city', 'created_at')
    list_editable = ('status',)
    search_fields = ('order_number', 'user__login', 'full_name', 'email', 'phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('order_number', 'user', 'status', 'payment_method', 'total_price')
        }),
        ('Данные покупателя', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Данные доставки', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Комментарии', {
            'fields': ('comment',),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'product_price', 'quantity', 'total_price')
    list_filter = ('order__status',)
    search_fields = ('order__order_number', 'product_name')
    
    def total_price(self, obj):
        return f"{obj.get_total_price()} ₽"
    total_price.short_description = 'Сумма'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__login', 'user__email')
    filter_horizontal = ('products',)
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество товаров'


# Опционально: можно добавить панель администрирования
admin.site.site_header = "PERFUME PALETTE | LUXE FRAGRANCE"
admin.site.site_title = "Администрирование парфюмерного магазина"
admin.site.index_title = "Панель управления"