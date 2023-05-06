from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, Store, Product_Photo, Product_Nutrition, Product_Ingredient

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass

class ImageInline(admin.TabularInline):
    model = Product_Photo
    fk_name = 'product'
    can_delete = False
    extra = 1

class NutritionInline(admin.TabularInline):
    model = Product_Nutrition
    fk_name = 'product'
    can_delete = False
    extra = 1

class IngredientInline(admin.TabularInline):
    model = Product_Ingredient
    fk_name = 'product'
    can_delete = False
    extra = 1

@admin.register(Product)
class ItemAdmin(admin.ModelAdmin):
    inlines = (NutritionInline, IngredientInline, ImageInline)
    search_fields = ['name']
    list_display = ['name', 'category', 'price', 'item_img']
    list_display_links = ['name']
    list_filter = ['category', 'status', 'created_at']

    def item_img(self, obj):
        img = obj.product_image.first()
        return mark_safe(f"<img src={img.photo.url} style='width: 100px;' />")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_displat = '__all__'
    list_displat_links = ['name']
