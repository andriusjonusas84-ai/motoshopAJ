from django.contrib.admin.utils import model_ngettext
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.views.generic.edit import FormMixin
from .forms import CustomUserCreationForm, ProductReviewForm
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

class ProductDetailView(FormMixin,generic.DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    form_class = ProductReviewForm

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse("product", kwargs={"pk": self.object.id})

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.product = self.get_object()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query)|
                                      Q(manufacturer__icontains=query)|
                                      Q(product_category__title__icontains=query)
                                     )
    produktu = Product.objects.filter(Q(title__icontains=query) |
                                      Q(manufacturer__icontains=query) |
                                      Q(product_category__title__icontains=query)
                                      ).count()
    context = {
        "query": query,
        "products": products,
        "produktu": produktu
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
    paginate_by = 6

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 6

class ProductListView1(generic.ListView):
    model = Product
    template_name = 'products1.html'
    context_object_name = 'products1'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(product_category=1)

class ProductListView2(generic.ListView):
    model = Product
    template_name = 'products2.html'
    context_object_name = 'products2'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(product_category=2)

class ProductListView3(generic.ListView):
    model = Product
    template_name = 'products3.html'
    context_object_name = 'products3'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(product_category=3)

class ProductListView4(generic.ListView):
    model = Product
    template_name = 'products4.html'
    context_object_name = 'products4'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(product_category=4)

class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = OrderLine
    template_name = 'orderline_form.html'
    fields = ['quantity']

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.order.pk})

    def test_func(self):
        return Order.objects.get(pk=self.get_object().order.pk).client == self.request.user

class OrderLineDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = OrderLine
    template_name = 'orderline_delete.html'
    context_object_name = 'orderline'

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.order.pk})

    def test_func(self):
        return Order.objects.get(pk=self.get_object().order.pk).client == self.request.user