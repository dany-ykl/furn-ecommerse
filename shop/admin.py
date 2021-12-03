from django.contrib import admin
from .models import Category, Product
from django.forms import ModelForm, ValidationError
from PIL import Image


class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name', 'price', 'stock', 'available')
    

class ProductAdminForm(ModelForm):
    min_height = 100
    min_width = 100
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = f'Min size image - {self.min_height}x{self.min_width}'

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        if img.height < self.min_height or img.width < self.min_width:
            raise ValidationError('Min size image 100x100')
        return image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'created', 'updated', 'category')
    list_filter = ('price', 'available', 'stock', 'category')
    search_fields = ['name']
    form = ProductAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'count']
    list_filter = ['name']
    search_fields = ['name']
    inlines = [ProductInline]

    
