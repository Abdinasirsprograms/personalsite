from django.db import models, transaction
from django.utils import timezone
from django.core.validators import MaxValueValidator
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import F
from django.core.mail import send_mail

from decimal import *
import os, datetime

class splash_post(models.Model):
        splash_heading = models.CharField(max_length=512)
        splash_img = models.CharField(max_length=512, blank=True)
        splash_bg_color = models.CharField(max_length=200, blank=True)
        splash_text = models.TextField(blank=True)

        class Meta:
            verbose_name = 'splash post'
            verbose_name_plural = 'splash posts'


class contact_me(models.Model):
        name_field = models.CharField(max_length=256)
        email_field = models.EmailField(max_length=254)
        message_text = models.TextField(max_length=1024)
        date_field = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ('date_field', )
            verbose_name = 'contact'
            verbose_name_plural = 'contacts'

        def __str__(self):
            return self.name_field

class blog_post(models.Model):
        heading_field = models.CharField(max_length=256)
        caption_field = models.CharField(max_length=254)
        body_text = models.TextField()
        date_field = models.TextField(max_length=12)

        class Meta:
            ordering = ('date_field', )
            verbose_name = 'blog post'
            verbose_name_plural = 'blog posts'

class category(models.Model):
        category_name = models.CharField(max_length=150, db_index=True)
        category_slug = models.SlugField(max_length=150, unique=True ,db_index=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
            ordering = ('category_name', )
            verbose_name = 'category'
            verbose_name_plural = 'categories'

        def __str__(self):
            return self.category_name


class product(models.Model):
        category = models.ForeignKey(category, related_name='product', on_delete=models.CASCADE)
        product_name = models.CharField(max_length=100, db_index=True)
        slug = models.SlugField(max_length=100, db_index=True)
        description = models.TextField(blank=True)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        available = models.BooleanField(default=True)
        stock = models.PositiveIntegerField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        def image_folder_path(self, instance):
            return os.path.join(instance.product_name, instance.product_name + ".jpeg")
        image = models.ImageField(upload_to=image_folder_path, blank=True)

        class Meta:
            ordering = ('product_name', )
            index_together = (('id', 'slug'),)

        def __str__(self):
            return self.product_name
class Product_images(models.Model):
        product_foreign = models.ForeignKey(product, related_name='Product_images', on_delete=models.CASCADE)
        def image_path(self, instance):
            # query = product.objects.filter('product_name').objects.all()
            return os.path.join(str(product.objects.get(id=(instance.product_foreign_id))).replace('product',''),
            instance.image_name + ".jpeg")
        product_images = models.ImageField(upload_to=image_path)
        image_name = models.CharField(max_length=100, db_index=True)
        slug = models.SlugField(max_length=100, db_index=True)

        class Meta:
            verbose_name = 'product images'
            verbose_name_plural = 'product images'

class Cart(models.Model):
        count = models.PositiveIntegerField(default=0)
        total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
        updated = models.DateTimeField(auto_now=True)
        timestamp = models.DateTimeField(auto_now_add=True)
        def __str__(self):
            return "sessions id {} has {} items in their cart. Their total is ${}".format(self.pk, self.count, self.total)

class Add_to_cart(models.Model):
        product_foreign = models.ForeignKey(product, related_name='Add_to_cart', on_delete=models.CASCADE)
        cart_foreign = models.ForeignKey(Cart, related_name='Add_to_cart', on_delete=models.CASCADE, default=1)
        quantity_of_product = models.PositiveIntegerField()
        def __str__(self):
            return "This cart entry contains {} {}(s).".format(self.quantity_of_product, self.product_foreign.product_name)

        class Meta:
            verbose_name = 'updated cart'
            verbose_name_plural = 'updated carts'

# @receiver(post_save, sender=Add_to_cart)
# def update_cart(sender, instance, **kwargs):
#     with transaction.atomic():
#         line_cost = instance.quantity_of_product * instance.product_foreign.price
#         cart_locked = Cart.objects.filter(id=instance.cart_foreign.id).select_for_update()
#         # stock_field = instance.product_foreign.stock
#         cart_locked.update(total= Decimal(line_cost))
#         cart_locked.update(count= instance.quantity_of_product)
#         cart_locked.update(updated= datetime.now())
#         # stock_field -= F(instance.cart_foreign.count)
class Reply(models.Model):
    email = models.ForeignKey(contact_me, related_name='Reply', on_delete=models.CASCADE)
    message = models.TextField()
    replied = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email.email_field)

class Email(models.Model):
    email_to = models.EmailField(max_length=254)
    subject_field = models.CharField(max_length=256)
    message_body = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email_to)

class Inbox(models.Model):
    message_id = models.CharField(max_length=250,unique=True)
    delivered_to = models.EmailField(max_length=254)
    email_from = models.EmailField(max_length=254)
    subject_field = models.CharField(max_length=256)
    message_body = models.TextField()
    date_received = models.DateTimeField(auto_now_add=True)
    original_date = models.DateTimeField()

    def __str__(self):
        return str(self.subject_field)

    class Meta:
        verbose_name = 'Inbox Email'
        verbose_name_plural = 'Inbox Emails'
        ordering = ('original_date',)


@receiver(post_save, sender=Email)
def send_email(sender, instance, **kwargs):
    email_address = instance.email_to
    subject = instance.subject_field
    body = instance.message_body
    origin_address = 'Abdinasir@abdinasirnoor.com'
    replied = instance.replied
    replied = True
    send_mail(
                subject,
                body,
                origin_address,
                [email_address],
                fail_silently=False,
            )

@receiver(post_save, sender=Inbox)
def send_notification(sender, instance, **kwargs):
    subject = 'New Email received'
    tm = instance.date_received
    tm = datetime.datetime.strftime(tm, "%c")
    body = "date: " + tm + " email from: " + instance.email_from + " subject: " + instance.subject_field + " message: " + instance.message_body
    origin_address = 'abdinasir@abdinasirnoor.com'
    send_mail(
                subject,
                ''.join(body),
                origin_address,
                ['abdinasirnoor@outlook.com',],
                fail_silently=False,
            )

@receiver(post_save, sender=Reply)
def send_reply_mail(sender, instance, **kwargs):
    contact_init = contact_me.objects.filter(id=instance.email.id)
    email_address = contact_init.values_list('email_field',flat=True).first()
    subject = 'RE: abdinasirnoor.com'
    body = instance.message
    origin_address = 'abdinasir@abdinasirnoor.com'
    replied = instance.replied
    replied = True
    send_mail(
                subject,
                body,
                origin_address,
                [email_address],
                fail_silently=False,
            )


@receiver(post_save, sender=Add_to_cart)
def update_cart(sender, instance, **kwargs):
    with transaction.atomic():
        cart_locked = Cart.objects.filter(id=instance.cart_foreign.id).select_for_update()
        line_cost = instance.quantity_of_product * instance.product_foreign.price
        total = Decimal(instance.cart_foreign.total) + Decimal(line_cost)
        count = instance.cart_foreign.count + instance.quantity_of_product
        cart_locked.update(total=total)
        cart_locked.update(count=count)
        cart_locked.update(updated= datetime.now())
        # instance.product_foreign.stock -= instance.cart_foreign.count
