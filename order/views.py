from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from cart.models import Cart, CartItem
from order.models import Order, OrderItem
from order.forms import BillingInformationForm, ShippingInformationForm, ShippingMethodForm, CreditCardForm, PaymentInformationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from order.models import BillingInformation, ShippingInformation, ShippingMethod, PaymentInformation, CreditCard

method_decorator(login_required, name="dispatch")


class CheckoutView(View):
    template_name = 'checkout.html'

    def get(self, request):
        # Получаем существующие данные пользователя
        billing_info = BillingInformation.objects.filter(
            user=request.user).first()
        shipping_info = ShippingInformation.objects.filter(
            user=request.user).first()
        credit_card_info = CreditCard.objects.filter(user=request.user).first()

        # Создаём формы с данными пользователя (если есть)
        billing_form = BillingInformationForm(instance=billing_info)
        shipping_form = ShippingInformationForm(instance=shipping_info)
        shipping_method_form = ShippingMethodForm(
            instance=shipping_info.shipping_method if shipping_info else None)
        credit_card_form = CreditCardForm(instance=credit_card_info)
        payment_form = PaymentInformationForm()

        cart = Cart.objects.get(user=request.user)

        return render(request, self.template_name, {
            'cart': cart,
            'billing_form': billing_form,
            'shipping_form': shipping_form,
            'shipping_method_form': shipping_method_form,
            'credit_card_form': credit_card_form,
            'payment_form': payment_form
        })

    def post(self, request):
        # Получаем существующие объекты
        billing_info = BillingInformation.objects.filter(
            user=request.user).first()
        shipping_info = ShippingInformation.objects.filter(
            user=request.user).first()
        credit_card_info = CreditCard.objects.filter(user=request.user).first()

        # Заполняем формы из POST-данных
        billing_form = BillingInformationForm(request.POST,
                                              instance=billing_info)
        shipping_form = ShippingInformationForm(request.POST,
                                                instance=shipping_info)
        shipping_method_form = ShippingMethodForm(request.POST,
                                                  instance=shipping_info.shipping_method if shipping_info else None)
        credit_card_form = CreditCardForm(request.POST,
                                          instance=credit_card_info)
        payment_form = PaymentInformationForm(request.POST)

        cart = Cart.objects.get(user=request.user)

        # Проверяем ВСЕ формы на валидность
        if (
                billing_form.is_valid() and
                shipping_form.is_valid() and
                shipping_method_form.is_valid() and
                payment_form.is_valid()
        ):
            # Сохраняем данные пользователя
            billing_info = billing_form.save(commit=False)
            billing_info.user = request.user
            billing_info.save()

            shipping_info = shipping_form.save(commit=False)
            shipping_info.user = request.user
            shipping_info.save()

            shipping_method = shipping_method_form.save(commit=False)
            shipping_method.shipping_info = shipping_info
            shipping_method.save()

            # Если выбрана оплата картой, проверяем её форму
            if payment_form.cleaned_data['method'] == "credit_card":
                if credit_card_form.is_valid():
                    credit_card = credit_card_form.save(commit=False)
                    credit_card.user = request.user
                    credit_card.save()
                else:
                    messages.error(request, "Ошибка в данных карты!")
                    return render(request, self.template_name, {
                        'cart': cart,
                        'billing_form': billing_form,
                        'shipping_form': shipping_form,
                        'shipping_method_form': shipping_method_form,
                        'credit_card_form': credit_card_form,
                        'payment_form': payment_form
                    })

            # Создаём заказ
            # Сохраняем данные из формы PaymentInformation
            # Присваиваем текущего пользователя перед сохранением PaymentInformation
            payment_info = payment_form.save(commit=False)
            payment_info.user = request.user
            payment_info.save()

            # Создаем заказ, передавая объект payment_info
            order = Order.objects.create(
                user=request.user,
                total_price=cart.get_total_price() + 45,
                # Добавляем стоимость доставки
                billing_info=billing_info,
                shipping_info=shipping_info,
                payment_info=payment_info

            )

            # Добавляем товары в заказ
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Очищаем корзину
            cart.items.all().delete()

            messages.success(request, "Ваш заказ успешно оформлен!")
            return redirect('index')

        messages.error(request, "Пожалуйста, исправьте ошибки в форме!")
        return render(request, self.template_name, {
            'cart': cart,
            'billing_form': billing_form,
            'shipping_form': shipping_form,
            'shipping_method_form': shipping_method_form,
            'credit_card_form': credit_card_form,
            'payment_form': payment_form
        })



