from django.urls import path
from main.views import IndexView, AboutUsView, BlogView, ContactView, BlogDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('blog/', BlogView.as_view(), name="blog"),
    path('blog/<int:id>/', BlogDetailView.as_view(), name='blog_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
]