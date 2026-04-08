from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/',views.search, name='search'),
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('profile/',views.ProfileChangeView.as_view(), name='profile'),
    path('orders/',views.MyOrdersListView.as_view(), name='myorders'),
    path('orders/<int:pk>',views.OrderDetailView.as_view(), name='order'),
    path('products/<int:pk>',views.ProductDetailView.as_view(), name='product'),
    path('products',views.ProductListView.as_view(), name='products'),
    path('categories/<int:product_category>',views.ProductCategoryListView.as_view(), name='products_category'),
    path('repair',views.repair,name='repair'),
    path('orderline/<int:pk>/update',views.OrderLineUpdateView.as_view(), name='orderline_update'),
    path('orderline/<int:pk>/delete',views.OrderLineDeleteView.as_view(), name='orderline_delete'),
]
