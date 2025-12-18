from django.db import migrations, models
import django.db.models.deletion

def reset_category_fields(apps, schema_editor):
    """Устанавливаем NULL для всех существующих записей"""
    Product = apps.get_model('shop', 'Product')
    # Очищаем поле category для всех продуктов
    Product.objects.all().update(category=None)
    
    # Если у вас есть старые значения в поле concentration, тоже очищаем
    # Product.objects.all().update(concentration='perfume')  # или устанавливаем дефолтное значение

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        # 1. Сначала делаем поле category nullable
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='shop.category',
                verbose_name='Категория',
                related_name='products'
            ),
        ),
        
        # 2. Обновляем поле concentration
        migrations.AlterField(
            model_name='product',
            name='concentration',
            field=models.CharField(
                choices=[
                    ('perfume', 'Парфюмерная вода (Eau de Parfum)'),
                    ('toilette', 'Туалетная вода (Eau de Toilette)'),
                    ('cologne', 'Одеколон (Eau de Cologne)'),
                    ('extrait', 'Экстракт (Extrait de Parfum)'),
                    ('body', 'Парфюмированное масло/лосьон')
                ],
                default='perfume',
                max_length=20,
                verbose_name='Концентрация'
            ),
        ),
        
        # 3. Запускаем функцию для очистки данных
        migrations.RunPython(reset_category_fields, migrations.RunPython.noop),
    ]