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
    path('products/motociklai',views.ProductListView1.as_view(), name='products1'),
    path('products/dalys',views.ProductListView2.as_view(), name='products2'),
    path('products/apranga',views.ProductListView3.as_view(), name='products3'),
    path('products/aksesuarai',views.ProductListView4.as_view(), name='products4'),
    path('repair',views.repair,name='repair'),
    path('orderline/<int:pk>/update',views.OrderLineUpdateView.as_view(), name='orderline_update'),
    path('orderline/<int:pk>/delete',views.OrderLineDeleteView.as_view(), name='orderline_delete'),
]
