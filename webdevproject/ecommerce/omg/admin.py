from django.contrib import admin
from .models import *

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on', 'image')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('user','name','email','phone')
    search_fields = ['user','name','email','phone']
    
class Product_Category_Admin(admin.ModelAdmin):
    list_display = ('category_id','category_name', 'created_on','updated_on')
    search_fields = ['category_name', 'category_id']
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_id','name', 'created_on','updated_on')
    search_fields = ['name', 'brand_id']
    
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_id','name','discount_amount', 'created_on','updated_on')
    search_fields = ['name', 'discount_id']
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','brand','name','category', "price", 'stock_status', 'created_on','updated_on')
    search_fields = ['name', 'product_id','SKU','category','brand']
    list_filter = ("brand","category",'stock_status')

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer','order','country','city','state','address','zipcode','created_on')
    search_fields = ['customer','order','country','city','state','address','zipcode','created_on']
    list_filter = ('customer','country','city','state','zipcode')
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('customer', 'transaction_id',"tracking_number", "ordered_on", "order_status", "complete")
    search_fields = ['customer', 'transaction_id', "complete", "ordered_on"]
    list_filter = ('customer',"complete")
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'created_on')
    search_fields = ['product', 'order', 'quantity', 'created_on']
    list_filter = ('order', 'product')
    
admin.site.register(News, NewsAdmin)
admin.site.register(Customer, CustomersAdmin)
#admin.site.register(Inventory)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Product_Category,Product_Category_Admin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order, OrdersAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Brand, BrandAdmin)