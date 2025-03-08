from django.urls import path
from cart.views import CartView, AddToCartView, RemoveFromCartView, ClearCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('clear/', ClearCartView.as_view(), name='clear_cart'),
]