import math

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max, Min
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import CustomUser, Product, Order, OrderLine, ProductCategory
from .filters import ProductFilter
from django_filters.views import FilterView
from .forms import CustomUserCreationForm, ProductReviewForm


def index(request):
    products = Product.objects.count()
    context = {
        'products': products,
    }
    return render(request,'index.html',context=context)

def repair(request):
    context = {
        'products':Product.objects.count(),
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

class ProductListView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'products.html'
    context_object_name = 'products'
    ordering = 'pk'

    paginate_by = 10

    def get(self, request, *args, **kwargs):
        original = request.GET
        cleaned = original.copy()

        # 1. Remove empty values for ALL fields
        for key in list(cleaned.keys()):
            if cleaned.get(key) in ("", None):
                cleaned.pop(key)

        # 2. Detect browser refresh
        cache_control = request.META.get("HTTP_CACHE_CONTROL", "")
        pragma = request.META.get("HTTP_PRAGMA", "")

        is_refresh = (
                "max-age=0" in cache_control
                or "no-cache" in cache_control
                or "no-cache" in pragma
        )

        if is_refresh and original:
            return redirect(request.path)

        # 3. Redirect ONLY if empty params were removed
        #    (Do NOT redirect when slider values exist)
        if original and original != cleaned:
            query = cleaned.urlencode()
            return redirect(f"{request.path}?{query}" if query else request.path)

        # 4. Normal processing
        return super().get(request, *args, **kwargs)

    def facet_queryset(self, filterset, exclude):
        # Prekės, atfiltruotos pagal visus filtrus, IŠSKYRUS nurodytus exclude sąraše
        data = filterset.data.copy()
        for name in exclude:
            data.pop(name, None)
        return self.filterset_class(data, queryset=self.get_queryset()).qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filterset = context["filter"]
        current_params = filterset.data.copy()

        price_qs = self.facet_queryset(filterset, ["final_price_0", "final_price_1"])
        prices = price_qs.aggregate(Min("final_price"), Max("final_price"))
        min_price = math.floor(prices["final_price__min"] or 0)
        max_price = math.ceil(prices["final_price__max"] or 0)
        if max_price <= min_price:
            max_price = min_price + 1

        active_filters = []

        BOOLEAN_LABELS = {
            "true": "Taip",
            "false": "Ne",
            "on": "Taip",
        }

        # Loop through filter fields IN ORDER
        for name, field in filterset.form.fields.items():

            # Special handling for price slider
            if name == "final_price":
                fp0 = self.request.GET.get("final_price_0")
                fp1 = self.request.GET.get("final_price_1")

                if fp0 and fp1:
                    new_params = current_params.copy()
                    new_params.pop("final_price_0", None)
                    new_params.pop("final_price_1", None)
                    remove_link = "?" + new_params.urlencode()

                    active_filters.append({
                        "label": "Pardavimo kaina",
                        "pairs": [(f"{fp0} – {fp1}", remove_link)],
                    })

                continue

            # Normal filters
            raw_values = current_params.getlist(name)
            raw_values = [v for v in raw_values if v]

            if not raw_values:
                continue

            label = field.label or name.replace("_", " ").title()

            display_values = []
            for v in raw_values:
                if v in BOOLEAN_LABELS:
                    display_values.append(BOOLEAN_LABELS[v])
                    continue

                try:
                    display_values.append(str(field.queryset.get(pk=v)))
                except:
                    display_values.append(v)

            pairs = []
            for v, display in zip(raw_values, display_values):
                new_params = current_params.copy()
                vals = new_params.getlist(name)
                vals.remove(v)
                new_params.setlist(name, vals)
                remove_link = "?" + new_params.urlencode()
                pairs.append((display, remove_link))

            active_filters.append({
                "label": label,
                "pairs": pairs,
            })

        # Gamintojai: tik tie, kurie yra tarp prekių pagal kitus filtrus
        manuf_qs = self.facet_queryset(filterset, ["manufacturer"])
        selected = filterset.data.getlist("manufacturer")
        names = set(manuf_qs.values_list("manufacturer", flat=True)) | set(selected)
        filterset.form.fields["manufacturer"].choices = [(m, m) for m in sorted(names, key=str.lower)]

        # Kategorijos: tik tos, kuriose yra prekių pagal kitus filtrus
        cat_qs = self.facet_queryset(filterset, ["product_category"])
        selected = filterset.data.getlist("product_category")
        ids = list(cat_qs.values_list("product_category", flat=True)) + selected
        context["filter_categories"] = ProductCategory.objects.filter(pk__in=ids).order_by("title")

        context["active_filters"] = active_filters
        context["max_price"] = max_price
        context["min_price"] = min_price

        return context

class ProductCategoryListView(ProductListView):
    template_name = 'products_category.html'

    def get_queryset(self):
        # Paimam ProductListView prekes ir paliekam tik šios kategorijos
        return super().get_queryset().filter(product_category=self.kwargs['product_category'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_title'] = ProductCategory.objects.get(pk=self.kwargs['product_category']).title
        return context


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
