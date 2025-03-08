from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from main.models import Main, AboutUs, Team, Blog, ContactUs
from product.models import Category, Product
from main.forms import ContactForm
from shop import settings
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main"] = Main.objects.latest('id')
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.order_by('-id')[:3]
        return context


class AboutUsView(TemplateView):
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_us'] = AboutUs.objects.latest('id')
        context['teams'] = Team.objects.all()
        context['categories'] = Category.objects.all()
        return context


class BlogView(ListView):
    queryset = Blog.objects.all()
    template_name = 'blog.html'
    context_object_name = 'blogs'
    paginate_by = 2


    def get(self, request, **args):
        query = request.GET.get('q')
        blogs = Blog.objects.filter(name__icontains=query) if query else Blog.objects.all()

        paginator = Paginator(blogs, self.paginate_by)
        page_number = request.GET.get('page')
        paginated_blogs = paginator.get_page(page_number)
        return render(request, self.template_name, {'blogs': paginated_blogs, 'query': query})



class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        form = ContactForm()
        contact = ContactUs.objects.latest('id')
        return render(request, self.template_name, {'form': form, 'contact': contact})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            send_mail(
                subject='Спасибо за ваше сообщение!',
                message='Мы получили ваше сообщение и ответим в ближайшее время.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[contact_message.email],
                fail_silently=False
            )
            messages.success(request, 'Ваше сообщение отправлено!')
            return redirect('contact')
        messages.error(request, 'Пожалуйста исправьте ошибку в форме!')
        return render(request, self.template_name, {'form': form})