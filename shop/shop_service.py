from typing import Dict, Any

from .models import Category, Product
from .mixins import get_cart_and_customer


@get_cart_and_customer
def get_products_list(request, *args, **kwargs) -> Dict[str, Any]:
    """Return products from category"""
    
    categories = Category.objects.all()

    sofa_category = categories.get(name='Sofa')
    sofa_list = sofa_category.get_products()

    table_category = categories.get(name='Table')
    table_list = table_category.get_products()

    chair_category = categories.get(name='Chair')
    chair_list = chair_category.get_products()

    bed_category = categories.get(name='Bed')
    bed_list = bed_category.get_products()

    decore_category = categories.get(name='Decore')
    decore_list = decore_category.get_products()

    products = Product.objects.all()

    context = {'sofa_list': sofa_list,
                'table_list': table_list,
                'chair_list': chair_list,
                'bed_list': bed_list,
                'decore_list': decore_list,
                'order': kwargs['order'],
                'products': products
                }
    
    return context
