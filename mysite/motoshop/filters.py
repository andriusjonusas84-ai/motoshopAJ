import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    final_price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = {'product_category': ['exact'],
                  'manufacturer': ['icontains'],
                  'stocked': ['exact']}