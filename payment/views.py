
from account.models import ShippingAddress
from core.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from basket.basket import Basket
import razorpay
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from order.views import view_order

# Create your views here.
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

@login_required
def payment_summary(request):
    
    basket = Basket(request)
    print(basket.basket.keys())
    amount = basket.total_product_price()
    global total
    total = amount
    user=str(request.user.id)
    
    callback_url = 'paymenthandler/'
    DATA = {
    "amount": total*100,
    "currency": "INR",
    "receipt": user,
    "payment_capture":'0'
    }
    order = client.order.create(dict(DATA))
    address = ShippingAddress.objects.filter(user=request.user, default=True)
    global order_id
    order_id = order['id']
    print(order)
    print(order['id'])
    
    return render(request, 'payment/payment_summary.html',{ 'order' : order, "address": address })



def paymenthandler(request):
    user= request.user.id
    print(user)
    use = request.POST.keys()
    print(use)
    basket = Basket(request)
    ab = request.POST['payment[razorpay_payment_id]']
    print(basket)
    address = request.POST['address']
    print(address)
    if request.method == "POST":
        try:
            payment_id = request.POST['payment[razorpay_payment_id]']
            razorpay_order_id = request.POST['payment[razorpay_order_id]']
            signature = request.POST['payment[razorpay_signature]']
            print(payment_id)
            print(razorpay_order_id)
            print(signature)
            result = client.utility.verify_payment_signature({
            'razorpay_order_id':razorpay_order_id,
            'razorpay_payment_id':payment_id,
            'razorpay_signature':signature
            })
            print(result)
            if result is True:
                data = {
                    "order_id": order_id,
                    "payment_id":payment_id,
                    "address":address,
                    "amount": total,
                    "user":user,
                    "basket":basket

                }
                view_order(data)
                Basket.clear(request)
                
                return render(request, 'payment/payment_success.html')
            else:

                return render(request, 'payment/payment_failed.html')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

    
     
    
       
       
    
   

