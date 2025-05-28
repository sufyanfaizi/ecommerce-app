from django.db import models
from django.shortcuts import get_object_or_404


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.objects.all().order_by('-last_updated')

    @classmethod
    def get_by_id(cls, product_id):
        return get_object_or_404(cls, id=product_id)

    @classmethod
    def get_by_sku(cls , sku):
        return cls.objects.get(sku=sku)

    @classmethod
    def update_quantity(cls , sku , quantity):
        product = get_object_or_404(cls,sku=sku)
        product.quantity = quantity
        product.save()

    @classmethod
    def create_product(cls, validated_data):
        return cls.objects.create(**validated_data)

    def update_product(self, validated_data):
        for attr, value in validated_data.items():
            setattr(self, attr, value)
        self.save()
        return self

    def delete_product(self):
        self.delete()
