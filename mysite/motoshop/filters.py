import django_filters
from .models import Product, ProductCategory
from django import forms
from .widgets import SliderRangeWidget
from django.db.models import Q


class ProductFilter(django_filters.FilterSet):
    product_category = django_filters.ModelMultipleChoiceFilter(
        queryset=ProductCategory.objects.all().order_by('title'),
        widget=forms.CheckboxSelectMultiple()
    )

    manufacturer = django_filters.MultipleChoiceFilter(
        choices=sorted(
            [(m, m) for m in Product.objects.values_list('manufacturer', flat=True).distinct()],
            key=lambda x: x[1].lower()
        ),
        widget=forms.CheckboxSelectMultiple()
    )


    final_price = django_filters.RangeFilter(field_name='final_price',
                                             method="filter_price",
                                             widget=SliderRangeWidget(min_value=0, max_value=10000, step=50),
                                             label="Pardavimo kaina, €"
    )

    stocked = django_filters.BooleanFilter(method='filter_checkbox', widget=forms.CheckboxInput, label='Sandėlio prekės')

    new_product = django_filters.BooleanFilter(method='filter_checkbox', widget=forms.CheckboxInput, label='Naujiena')

    def filter_checkbox(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: True})
        return queryset

    q = django_filters.CharFilter(method='filter_search', label='Paieška')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(manufacturer__icontains=value) |
            Q(product_category__title__icontains=value)
        )

    def filter_price(self, queryset, name, value):

        if not value:
            return queryset

        if isinstance(value, slice):
            low, high = value.start, value.stop
        elif hasattr(value, "start") and hasattr(value, "stop"):
            low, high = value.start, value.stop
        elif isinstance(value, (list, tuple)) and len(value) == 2:
            low, high = value
        else:
            return queryset

        try:
            low = float(low) if low not in ("", None) else None
            high = float(high) if high not in ("", None) else None
        except:
            return queryset

        # 👉 skip when full default range
        if low == 0 and high == 10000:
            return queryset

        if low is not None and high is not None:
            return queryset.filter(final_price__gte=low, final_price__lte=high)

        return queryset


    class Meta:
        model = Product
        fields = ('product_category', 'manufacturer', 'stocked', 'final_price','new_product')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.label_suffix = ""
