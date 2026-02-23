from django.contrib.admin.utils import model_ngettext
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView

from .models import CustomUser,Product,Order,OrderLine,Post,Comment

def index(request):
    context = {
        'products':Product.objects.count()
    }
    return render(request,'index.html',context=context)


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query)|
                                     Q(manufacturer__icontains=query)
                                     )

    context = {
        "query": query,
        "products": products,

    }
    return render(request, template_name="search.html",context=context)


