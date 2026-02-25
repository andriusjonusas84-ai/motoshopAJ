from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Order, OrderLine, Post, Comment, ProductCategory



class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': ('photo',)}),
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'manufacturer','stock_quantity','stocked','new_product','final_price']
    list_filter = ('manufacturer', 'stocked','category')
    search_fields = ('manufacturer', 'stocked')

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order__id', 'product_category','product__title','product__code', 'product__rrp','product__final_price','quantity','order_line_sum')

    fieldsets = [
        ('Pagrindinė informacija', {'fields': ['order','product_category','product','quantity'],
                     }),
    ]

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ['order_line_sum']
    extra = 0
    fields = ['product_category','product','quantity','order_line_sum']

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderLineInline]
    list_display = ['pk','order_date','client','status','due_date']
    readonly_fields = ['order_sum']

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk','title']



admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ProductCategory,ProductCategoryAdmin)

