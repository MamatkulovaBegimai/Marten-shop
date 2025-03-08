from django.urls import path
from product.views import ProductListView, ProductDetailView, CategoryProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name="products"),
    path('<int:id>/', ProductDetailView.as_view(), name="product_detail"),
    path('category/<int:category_id>/',
         CategoryProductListView.as_view(), name="category_products"),
]