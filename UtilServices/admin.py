from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from UtilServices.models import *

# Register your models here.

# admin.site.register(Customer)
# admin.site.register(Product)
# admin.site.register(Cart)
# admin.site.register(OrderPlaced)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','name','selling_price','discount_price','description','brand','category','product_image']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','customer','customer_info','product','product_info','quantity','order_date','status']


    def customer_info(self,obj):
        link=reverse("admin:UtilServices_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    
    def product_info(self,obj):
        link=reverse("admin:UtilServices_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.name)

