from django.db import models
from user.models import CustomUser
from product.models import Product
# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    addad_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Избранные'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
