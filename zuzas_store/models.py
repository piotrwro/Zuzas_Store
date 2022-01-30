from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
TYPE = (
    (1, "Szkło"),
    (2, "Malarstwo"),
    (3, "Rzeźba"),
    (4, "Haft"),

)


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=16, blank=True, null=True,
                                    validators=[RegexValidator(regex=r"^\+?1?\d{8,15}$")])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=64)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.IntegerField()
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name


class Property(models.Model):
    type = models.IntegerField(choices=TYPE)
    height = models.IntegerField()
    width = models.IntegerField()
    thickness = models.IntegerField()
    technique = models.CharField(max_length=255,
                                 help_text='Wpisz technikę wykonania(np. obraz olejny, szkło grawerowane)')
    base_material = models.CharField(max_length=255, help_text='Wpisz materiał bazowy(np. płótno, karton, itp.')
    product = models.OneToOneField('Product', on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.product.name}'


class Images(models.Model):
    image = models.ImageField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.image}'


class CartOrder(models.Model):
    user = models.ForeignKey('UserProfile', null=True, on_delete=models.CASCADE, related_name="user_cart_order")
    is_paid = models.BooleanField(default=False)
    product = models.ManyToManyField('Product', through='CartOrderProduct')
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f'CartOrder {self.user}'


class CartOrderProduct(models.Model):
    product = models.ForeignKey('Product', related_name='order_items', on_delete=models.CASCADE)
    cart_order = models.ForeignKey("CartOrder",  related_name='items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.product)
