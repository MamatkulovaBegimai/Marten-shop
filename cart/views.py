from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from product.models import Product
from cart.models import Cart, CartItem
# Create your views here.


class CartView(LoginRequiredMixin, View):
    template_name = 'cart.html'

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'cart': cart})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, 'Количество тавара увеличено')
        else:
            messages.success(request, 'Товар добавлен в корзину')
        return redirect('cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, 'Товар удален из корзины')
        return redirect('cart')


class ClearCartView(LoginRequiredMixin, View):
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
            messages.success(request, 'Корзина очищена')
        return redirect('cart')