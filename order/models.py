from django.db import models
from user.models import CustomUser
from product.models import Product
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} * {self.product.name} in order {self.order.id}"


class BillingInformation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="billing_information")
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return f"Billing Info for {self.user.username}"


class ShippingInformation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="shipping_information")
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    use_billing_information = models.BooleanField(default=True)

    def __str__(self):
        return f"Shipping Info for {self.user.username}"

class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price} сом"

class PaymentInformation(models.Model):
    METHOD_CHOICES = [
        ('money_order', 'Check/Money Order'),
        ('credit_card', 'Credit Card'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=255, choices=METHOD_CHOICES, default="money_order")

class CreditCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="credit_card")
    card_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=20, choices=[
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
    ])
    card_number = models.CharField(max_length=16)
    expiration_month = models.PositiveSmallIntegerField()
    expiration_year = models.PositiveSmallIntegerField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.card_type} - {self.user.username}"



