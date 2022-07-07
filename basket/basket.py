


from store.models import Product


class Basket():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, product_qty):
        product_id = product.id

        if product_id in self.basket:
            self.basket[product_id] = product_qty
        else:
            self.basket[product_id] = { 'price': int(product.price), 'qty': int(product_qty)}

        self.session.modified = True

    def delete(self,product):
        product_id = product.id

        del self.basket[str(product_id)]
        self.session.modified = True

    def update(self, product, product_qty):
        product_id = str(product.id)
        

        if product_id in self.basket:
            self.basket[product_id]['qty']= product_qty  
        self.session.modified = True

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product
        for item in self.basket.values():
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def total_product_price(self):
        return sum(item['qty'] * item['price'] for item in self.basket.values())

    def total_price(self,product_id):

        product_id= str(product_id)
        return self.basket[product_id]['qty'] * self.basket[product_id]['price']

    def clear(self):
        
        del self.session['skey']
        self.session.modified = True
         