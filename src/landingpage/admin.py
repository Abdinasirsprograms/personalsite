from django.contrib import admin
from .models import *

from django.utils.safestring import mark_safe

class ReadDate(admin.ModelAdmin):
    readonly_fields = ('date_field',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'category_slug']
    prepopulated_fields = {'category_slug': ('category_name',)}
    
class Product_images_admin(admin.TabularInline):
    model = Product_images
    prepopulated_fields = {'slug': ('image_name',)}
    readonly_fields = ["current_image"]
    def current_image(self,obj):
        return mark_safe('<img src="{url}" width="40%" height="40%" />'.format(
            url = obj.product_images.url,
            )
    )
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        Product_images_admin,
    ]
    list_display = ['product_name', 'description', 'price', 'available', 'stock', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('product_name',)}
    readonly_fields = ["current_image"]
    def current_image(self,obj):
        return mark_safe('<img src="{url}" width="50%" height="50%" />'.format(
            url = obj.image.url,
            )
    )
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('updated','timestamp',)

class ReplyAdmin(admin.TabularInline):
    model = Reply

@admin.register(contact_me)
class ContactMeAdmin(admin.ModelAdmin):
    readonly_fields = ('date_field',)
    inlines = [
        ReplyAdmin,
    ]
@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
    model = Inbox
    ordering = ('-original_date',)
    list_display = ('subject_field','original_date',)
    readonly_fields = ("date_received","original_date",)

admin.site.register(splash_post)
admin.site.register(blog_post)
admin.site.register(category, CategoryAdmin)
admin.site.register(product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Add_to_cart)
admin.site.register(Email)
