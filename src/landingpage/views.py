from django.shortcuts import render
from django.conf import settings
from .models import *
from .forms import post_form, Post_add_to_cart
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
import random
import urllib
import urllib.request
import json

def homepage(request):
        return render(request, 'landingpage/index.html')

def contacted(request):
        if request.method == 'POST':
                form = post_form(request.POST)
                if form.is_valid():
                   # get the token submitted in the form
                    recaptcha_response = request.POST.get('g-recaptcha-response')
                    url = 'https://www.google.com/recaptcha/api/siteverify'
                    payload = {
                        'secret': settings.RECAPTCHA_SECRET_KEY,
                        'response': recaptcha_response
                    }
                    data = urllib.parse.urlencode(payload).encode()
                    req = urllib.request.Request(url, data=data)

                    # verify the token submitted with the form is valid
                    response = urllib.request.urlopen(req)
                    result = json.loads(response.read().decode())

                    # result will be a dict containing 'success' and 'action'.
                    # it is important to verify both
                    if 'error_codes' in result.keys():
                        errorCodes = result['error_codes']
                    else:
                        errorCodes = 'None'
                    if (result['success'] == 'false') or (not result['action'] == 'contactForm') or (result['score'] <= 0.5):  # make sure action matches the one from your template
                        return(JsonResponse({'form_sent':'false', 'botdetected': 'true', 'error_codes': f'{errorCodes}',}), HttpResponse(status=401))

                    form.save()
                    return(JsonResponse({'form_sent':'true', 'botdetected': 'false'}))
        else:
           return(JsonResponse({'data':'no data posted'}))



def sitemap(request):
        return HttpResponseRedirect('http://abdinasirnoor.com/static/landingpage/sitemap.xml')

def privacy(request):
        return render(request,'landingpage/base/privacy.html')

def eccomerce(request):
        query = product.objects.filter(available=True)
        if 'cart_id' not in request.session:
            request.session['cart_id'] = random.randrange(1,1000)
            cart_id_saved = request.session['cart_id']
            products_added_already = []
            cart_info = 0
        else:
            cart_id_saved = request.session['cart_id']
            cart_items = Add_to_cart.objects.filter(cart_foreign=cart_id_saved).values_list('product_foreign',flat=True).distinct()
            products_added_already = [x for x in cart_items]
            cart_info = Cart.objects.filter(pk=cart_id_saved)
            if cart_info:
                cart_info = cart_info.values('count').get()['count']
            else:
                cart_info = 0
        return render(request,'eccomerce/base.html',context={"products":query,"cart":cart_info,"products_added":products_added_already})

def Push_to_cart(request, pk):
        value = request.session['cart_id']
        my_cart = Cart.objects.get_or_create(pk=value)
        cart_info = Cart.objects.filter(pk=value).count()
        product_obj = product.objects.get(id=pk)
        product_amount = request.POST.get('quantity_of_product')
        if request.method == 'POST':
            add_to_cart_obj = Add_to_cart(product_foreign=product_obj,
            cart_foreign=my_cart[0], quantity_of_product=int(product_amount))
            add_to_cart_obj.save()
            cart_info = Cart.objects.filter(pk=value).values('count').get()['count']
            return JsonResponse({'Data sent':'Successfully','cart_count_update':cart_info,})
        form = Post_add_to_cart()
        cart_info = 0
        return JsonResponse({'form':'Not sent','cart_count_update':cart_info,})

def product_view(request, slug):
        query = get_object_or_404(product, slug=slug)
        query_product_id = product.objects.all().filter(slug=slug).values('id').get()
        query_unclean_image = Product_images.objects.all().filter(product_foreign=query_product_id['id'])
        query_image = []
        for obj in query_unclean_image:
            query_image = list(query_unclean_image.values('product_images'))
        query_data = {'query':query,'query_image':query_image, 'query_product_id': query_product_id,}
        context = {'product': query_data}
        return render(request,'landingpage/product_view.html',context)

def Cart_view(request):
    value = request.session['cart_id']
    cart_obj = Cart.objects.filter(pk=value)
    if cart_obj:
        cart_count = Cart.objects.filter(pk=value).values('count').get()['count']
        cart_obj = Add_to_cart.objects.filter(cart_foreign=value).distinct().values_list('product_foreign',flat=True)
        cart_obj = [x for x in cart_obj]
        products_in_cart = []
        product_quantities = []
        for x in cart_obj:
            products_in_cart.append(product.objects.get(id=x))
            product_quantities.append(Add_to_cart.objects.filter(product_foreign=x,cart_foreign=value).aggregate(Sum('quantity_of_product'))['quantity_of_product__sum'])
        merged = products_in_cart + product_quantities
        context = {'cart':cart_obj,'cart_count':cart_count,'products':products_in_cart,'product_numbers':product_quantities,'merged_item':merged}
    else:
        cart_obj = None
        context = {'cart':cart_obj}
    return render(request,'landingpage/cart.html',context)
#
#     if request.POST:
#         # Get the product's ID from the POST request.
#         product_foreign = request.POST.get('product_foreign')
#         # Get the object using our unique primary key
#         product_foreign_obj = product.objects.get(id=product_foreign)
#         # Get the quantity of the product desired.
#         product_quantity = request.POST.get('product_quantity')
#         # Create the new Entry...this will update the cart on creation
#         Add_to_cart.objects.create(cart=my_cart, product=product_foreign, quantity=product_quantity)
#         return JsonResponse({'Data sent':'Successfully','product_foreign':product_foreign,
#         'product_quantity':product_quantity,})
#     else:
#         return JsonResponse({'form':'Not sent'})

'''
def product_list(request, category_slug=None):
    category = None
    categories = category.objects.all()
    products = product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(category, slug=category_slug)
        products = product.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(product, id=id, slug=slug, available=True)
    context = {
        'product': product
    }
    return render(request, 'shop/product/detail.html', context)
'''
