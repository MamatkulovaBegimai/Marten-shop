from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from cart.models import Cart
from order.models import Order, OrderItem
from order.forms import BillingInformationForm, ShippingInformationForm, ShippingMethodForm, CreditCardForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    template_name = 'checkout.html'

    def get(self, request):
        cart = Cart.objects.get(user=request.user)

        billing_form = BillingInformationForm(instance=getattr(request.user, 'billing_information', None))
        shipping_information_form = ShippingInformationForm(instance=getattr(request.user, 'shipping_information', None))
        shipping_method_form = ShippingMethodForm(instance=getattr(request.user, 'shipping_method', None))
        credit_card_form = CreditCardForm(instance=getattr(request.user, 'credit_card', None))
        return render(request, self.template_name, {
            'cart': cart,
            'billing_form': billing_form,
            'shipping_information_form': shipping_information_form,
            'shipping_method': shipping_method_form,
            'credit_card_form': credit_card_form
        })

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.error(request,"Ваша корзина пуста!")
            return redirect('cart')

        billing_form = BillingInformationForm(request.POST, instance=getattr(
            request.user, 'billing_information', None))
        shipping_information_form = ShippingInformationForm(
            instance=getattr(request.POST, 'shipping_information', None))
        shipping_method_form = ShippingMethodForm(
            instance=getattr(request.POST, 'shipping_method', None))
        credit_card_form = CreditCardForm(
            instance=getattr(request.POST, 'credit_card', None))

        if all([billing_form.is_valid(), shipping_information_form.is_valid(),
               shipping_method_form.is_valid(), credit_card_form.is_valid()]):
            billing_info = billing_form.save(commit=False)
            billing_info.user = request.user
            billing_info.save()

            shipping_info = shipping_information_form.save(commit=False)
            shipping_info.user = request.user
            shipping_info.save()

            shipping_method_info = shipping_method_form.save(commit=False)
            shipping_method_info.user = request.user
            shipping_method_info.save()

            credit_card_info = credit_card_form.save(commit=False)
            credit_card_info.user = request.user
            credit_card_info.save()

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

        return render(request, self.template_name, {
            'cart': cart,
            'billing_form': billing_form,
            'shipping_information_form': shipping_information_form,
            'shipping_method': shipping_method_form,
            'credit_card_form': credit_card_form})


