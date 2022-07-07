from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from basket.basket import Basket
from store.models import Product

# Create your views here.
def basket_summary(request):
    return render(request, 'store/basket/summary.html')

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404( Product , id=product_id)
        basket.add(product= product, product_qty = product_qty)
        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = (request.POST.get('productid'))
        print(product_id)
        product = get_object_or_404( Product , id=product_id)
        basket.delete(product= product)
        basket_qty = basket.__len__()
        subtotal = basket.total_product_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': subtotal})
        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404( Product , id=product_id)
        basket.update(product= product, product_qty = product_qty)
        basket_qty = basket.__len__()
        total =basket.total_price(product_id)
        subtotal = basket.total_product_price()
        response = JsonResponse({'qty': basket_qty,'subtotal': subtotal, 'total': total})
        return response
