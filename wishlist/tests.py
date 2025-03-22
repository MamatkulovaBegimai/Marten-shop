from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cart, Order, OrderItem
from .forms import BillingInformationForm, ShippingInformationForm, \
    PaymentInformationForm, CreditCardForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    template_name = 'checkout.html'

    def get(self, request):
        cart = Cart.objects.get(user=request.user)

        # Создаём формы с уже сохранёнными данными пользователя (если есть)
        billing_form = BillingInformationForm(
            instance=getattr(request.user, 'billing_information', None))
        shipping_form = ShippingInformationForm(
            instance=getattr(request.user, 'shipping_information', None))
        payment_form = PaymentInformationForm()
        credit_card_form = CreditCardForm()

        return render(request, self.template_name, {
            'cart': cart,
            'billing_form': billing_form,
            'shipping_form': shipping_form,
            'payment_form': payment_form,
            'credit_card_form': credit_card_form,
        })

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.error(request, "Ваша корзина пуста!")
            return redirect('cart')

        billing_form = BillingInformationForm(request.POST,
                                              instance=getattr(request.user,
                                                               'billing_information',
                                                               None))
        shipping_form = ShippingInformationForm(request.POST,
                                                instance=getattr(request.user,
                                                                 'shipping_information',
                                                                 None))
        payment_form = PaymentInformationForm(request.POST)
        credit_card_form = CreditCardForm(request.POST)

        if all([billing_form.is_valid(), shipping_form.is_valid(),
                payment_form.is_valid(), credit_card_form.is_valid()]):
            # Сохраняем информацию о биллинге
            billing_info = billing_form.save(commit=False)
            billing_info.user = request.user
            billing_info.save()

            # Сохраняем информацию о доставке
            shipping_info = shipping_form.save(commit=False)
            shipping_info.user = request.user
            shipping_info.save()

            # Сохраняем информацию об оплате
            payment_info = payment_form.save(commit=False)
            payment_info.user = request.user
            payment_info.save()

            # Если выбрана оплата картой, сохраняем данные карты
            if payment_info.method == 'credit_card':
                credit_card = credit_card_form.save(commit=False)
                credit_card.user = request.user
                credit_card.save()

            # Создаём заказ
            order = Order.objects.create(user=request.user, total_price=sum(
                item.total_price for item in cart.items.all()))
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Очищаем корзину
            cart.items.all().delete()

            messages.success(request, 'Ваш заказ успешно оформлен!')
            return redirect('index')

        # Если формы не валидны, возвращаем их с ошибками
        return render(request, self.template_name, {
            'cart': cart,
            'billing_form': billing_form,
            'shipping_form': shipping_form,
            'payment_form': payment_form,
            'credit_card_form': credit_card_form,
        })
