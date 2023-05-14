from django.contrib import admin
from .models import *

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on', 'image')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
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
    
admin.site.register(News, NewsAdmin)
admin.site.register(Customer)
#admin.site.register(Inventory)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Product_Category,Product_Category_Admin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Brand, BrandAdmin)