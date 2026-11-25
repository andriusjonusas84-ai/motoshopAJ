from decimal import Decimal

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def price(value):
    try:
        value = Decimal(value)
    except Exception:
        return value
    whole, cents = f'{value:,.2f}'.split('.')
    whole = whole.replace(',', '&nbsp;')
    return mark_safe(f'{whole}<sup>{cents}</sup>')