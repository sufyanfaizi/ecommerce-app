from .models import Product

class ProductService:
    def get_all(self):
        return Product.get_all()

    def get_by_id(self, product_id):
        return Product.get_by_id(product_id)

    def create(self, validated_data):
        return Product.create_product(validated_data)

    def update(self, product, validated_data):
        return product.update_product(validated_data)

    def delete(self, product):
        product.delete_product()
