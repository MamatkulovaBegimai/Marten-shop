from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from cart.models import Cart
from order.models import Order, OrderItem


# Create your views here.
class CheckoutView(View):
    template_name = 'checkout.html'

    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        return render(request, self.template_name, {'cart': cart})

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.error(request,"Ваша корзина пуста!")
            return redirect('cart')

        order = Order.objects.create(user=request.user, total_price=sum(item.total_price for item in cart.items.all()))
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()
        messages.success(request, 'Ваш заказ успешно оформлен!')
        return redirect('index')
