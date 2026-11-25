from .models import ProductCategory


def category_context(request):
    favorite_ids = []
    cart_product_count = 0
    cart_preview = []
    cart_sum = 0
    if request.user.is_authenticated:
        favorite_ids = list(request.user.favorites.values_list('pk', flat=True))
        lines = list(request.user.cart_lines.select_related('product').order_by('-pk'))
        cart_product_count = len(lines)
        cart_preview = lines[:3]
        cart_sum = sum(line.cart_line_sum() for line in lines)
    return {
        'categories': ProductCategory.objects.all().order_by('title'),
        'favorite_ids': favorite_ids,
        'cart_product_count': cart_product_count,
        'cart_preview': cart_preview,
        'cart_sum': cart_sum,
    }