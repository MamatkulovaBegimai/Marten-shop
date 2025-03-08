from django.urls import path
from wishlist.views import AddToWishlistView, WishlistView, RemoveFromWishlistView


urlpatterns = [
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:product_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist')
]