from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name = models.CharField("Название", max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product', verbose_name="Категория продукта")
    photo = models.ImageField("Фотография", upload_to='product_photo')
    slug = models.SlugField("Человекопонятный URL", unique=True, blank=True)
    price = models.CharField("Цена", max_length=50)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"id": self.id})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"