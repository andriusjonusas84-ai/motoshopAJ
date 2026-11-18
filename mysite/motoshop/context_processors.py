from .models import ProductCategory

def category_context(request):
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(request.user.favorites.values_list('pk', flat=True))
    return {
        'categories': ProductCategory.objects.all().order_by('title'),
        'favorite_ids': favorite_ids,
    }