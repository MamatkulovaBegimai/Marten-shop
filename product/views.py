from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404

from product.models import Category, Product
# Create your views here.


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = "products"
    template_name = "shop-page.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get(self, request, **args):
        query = request.GET.get('q')
        products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()

        paginator = Paginator(products, self.paginate_by)
        page_number = request.GET.get('page')
        paginated_products = paginator.get_page(page_number)
        return render(request, self.template_name, {'products': paginated_products, 'query': query})


class ProductDetailView(DetailView):
    model = Product
    template_name = "product-details.html"
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        return context

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Product, id=id)


class CategoryProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'category.html'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category_id'])
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context