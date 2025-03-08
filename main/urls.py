from django.urls import path
from main.views import IndexView, AboutUsView, BlogView, ContactView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('blog/', BlogView.as_view(), name="blog"),
    path('contact/', ContactView.as_view(), name='contact'),
]