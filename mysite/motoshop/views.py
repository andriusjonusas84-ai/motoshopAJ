from django.contrib.admin.utils import model_ngettext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django import forms

from .models import CustomUser,Product,Order,OrderLine,Post,Comment

def index(request):
    context = {
        'products':Product.objects.count()
    }
    return render(request,'index.html',context=context)

def repair(request):
    context = {
        'products':Product.objects.count()
    }
    return render(request,'repair.html',context=context)

def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query)|
                                      Q(manufacturer__icontains=query)|
                                      Q(product_category__title__icontains=query)
                                     )
    context = {
        "query": query,
        "products": products,
    }
    return render(request, template_name="search.html",context=context)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

class ProfileChangeView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    template_name = 'profile.html'
    success_url = reverse_lazy('index')
    fields = ['first_name','last_name','email','photo']

    def get_object(self, queryset=None):
        return self.request.user

class MyOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'myorders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)
