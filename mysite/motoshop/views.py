from django.contrib.admin.utils import model_ngettext
from django.shortcuts import render
from .models import CustomUser,Product,Order,OrderLine,Post,Comment

def index(request):
    context = {
        'products':Product.objects.count()
    }
    return render(request,'index.html',context=context)