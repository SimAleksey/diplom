from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(null=True, verbose_name='Слаг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание')
    shopping = models.PositiveIntegerField(default=0, verbose_name='Количество покупок')
    preview = models.ImageField(upload_to='images/product/previews/', blank=True, null=True, verbose_name='Превью')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='product')
    producer = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Производитель', related_name='product',
                                 null=True)
    slug = models.SlugField(blank=True)
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    color = models.TextField(max_length=100, verbose_name='Цвет')
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)
        return self.price


class Color(models.Model):
    color = models.TextField(max_length=100, verbose_name='Цвет')
    product_parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество товара')
    shopping = models.PositiveIntegerField(default=0, verbose_name='Количество покупок')
    preview = models.ImageField(upload_to='images/product/previews/', blank=True, null=True, verbose_name='Превью')
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка')

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)
        return self.price


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', related_name='comments')
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.product.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.JSONField(default=list)


class StorageQueryset(models.QuerySet):

    def total_price(self):
        a = 0
        b = 0
        color = []
        product = []
        for i in self:
            if i.product:
                product.append(i.product_price())
            else:
                product.append(i.product_color_price())
        for price in product:
            a += price
        for price in color:
            b += price
        return a + b

    def total_quantity(self):
        if self:
            return sum(storage.quantity for storage in self)

        return 0


class Storage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', null=True)
    product_color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name='Продукт', null=True)
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количеcтво')

    def __str__(self):
        if self.product:
            return f'Корзина {self.user.username} Товар {self.product.title} Количество {self.quantity}'
        else:
            return f'Корзина {self.user.username} Товар {self.product_color.product_parent}/{self.product_color.color} Количество {self.quantity}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    objects = StorageQueryset().as_manager()

    def product_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def product_color_price(self):
        return round(self.product_color.sell_price() * self.quantity, 2)