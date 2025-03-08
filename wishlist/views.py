from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages

from wishlist.models import Wishlist
from product.models import Product
# Create your views here.

class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, 'Товар добавлен в избранное!')
        else:
            messages.info(request, "Товар уже в избранном.")
        return redirect('products')


class WishlistView(LoginRequiredMixin, View):
    template_name = 'wishlist.html'

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return render(request, self.template_name, {'wishlist_items': wishlist_items})


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Wishlist.objects.filter(user=request.user, product=product).delete()
        messages.success(request, "Товар удален из избранного")
        return redirect('wishlist')