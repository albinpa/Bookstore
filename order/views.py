from django.shortcuts import render
from account.models import ShippingAddress

from store.models import Product
from .models import Order, OrderItem
from basket.basket import Basket 
from django.contrib.auth.decorators import login_required
# Create your views here.

def view_order(request):
    
    print('123')
    print (request.keys())
    print(request['order_id'])
    order_id = request['order_id']
    payment_id = request['payment_id']
    amount = request['amount']
    address = int(request['address'])
    print('23')
    user = int(request['user'])
    
    print (user)
    basket = request['basket']
    

    if Order.objects.filter(order_key=order_id).exists():
        pass
    else:
        order = Order.objects.create(order_key=order_id, payment_id=payment_id, user_id=user, shipp_addr_id=address, amount=amount, billing_status=True)
        orderid = order.pk
        print('12333')
        product_ids=basket.basket.keys()
        
        for i in product_ids:
            product_id=int(i)
            product = basket.basket[str(i)]
            price = product['price']
            quantity = product['qty']
            
            OrderItem.objects.create(order_id= orderid, product_id= product_id ,price= price,quantity= quantity)
            
def orders(request):
    
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        address=order.shipp_addr
        print(address.state)
        orderid = order.pk
        print(orderid)
        prod_details = OrderItem.objects.filter(order=orderid)
        print (prod_details.values())
        for product in prod_details:
            pass
    return render(request, 'store/orders/order.html',{"order": orders, "address": address, "product": product})
        
        
       
        
            
                
                

            