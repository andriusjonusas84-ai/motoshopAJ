import django_filters
from .models import Product, ProductCategory
from django import forms
from django_filters.widgets import BooleanWidget, RangeWidget
from django.utils.translation import gettext as _

class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the choices: (value, label)
        self.choices = (
            ("", _("--------")),
            ("true", _("Taip")),
            ("false", _("Ne"))
        )

class CustomRangeWidget(RangeWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        # Customize the "Start" (Min) field
        self.widgets[0].attrs.update({
            'placeholder': 'Nuo',
            'size': '5px',  # Sets the 'size' attribute (visual length)
            'class': 'min-field-class'
        })
        # Customize the "End" (Max) field
        self.widgets[1].attrs.update({
            'placeholder': 'Iki',
            'size': '5px',
            'style': 'margin-left: 3px',
            'class': 'max-field-class'
        })
class ProductFilter(django_filters.FilterSet):
    product_category = django_filters.ModelMultipleChoiceFilter(queryset=ProductCategory.objects.all(),
                                                                widget=forms.CheckboxSelectMultiple(
                                                                    attrs={'class': 'select2-dropdown'})
                                                                )
    manufacturer = django_filters.CharFilter(lookup_expr='icontains',
                                            widget=forms.TextInput(attrs={'placeholder': 'Įveskite gamintoją'})
                                            )
    final_price = django_filters.RangeFilter(widget=CustomRangeWidget)

    stocked = django_filters.BooleanFilter(widget=CustomBooleanWidget)

    class Meta:
        model = Product
        fields = ('product_category', 'manufacturer','stocked','final_price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Access the auto-generated form and remove the colon
        self.form.label_suffix = ""
