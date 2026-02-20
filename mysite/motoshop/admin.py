from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Order, OrderLine, Post, Comment


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': ('photo',)}),
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'manufacturer','stock_quantity','stocked','new_product','final_price']
    list_filter = ('manufacturer', 'stocked','category')
    search_fields = ('manufacturer', 'stocked')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Post)
admin.site.register(Comment)

