from django.contrib import admin

# Register your models here.
from zuzas_store.models import UserProfile, Category, Product, Images, Property, CartOrder, CartOrderProduct

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Property)
admin.site.register(Images)
admin.site.register(CartOrder)
admin.site.register(CartOrderProduct)
