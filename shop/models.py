from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def get_products(self):
         return Product.objects.filter(category=self, available=True)

    def count(self):
        return Product.objects.filter(category=self).count()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=3000)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    slug = models.SlugField(max_length=60, default='')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product-detail', args=[str(self.slug,)])
    
    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.available = False
        return super().save(*args, **kwargs)