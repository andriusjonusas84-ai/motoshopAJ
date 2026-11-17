from .models import ProductCategory

def category_context(request):
    return {
        'categories': ProductCategory.objects.all().order_by('title'),
    }