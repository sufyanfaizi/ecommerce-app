from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField


def increase_price(queryset, percentage=10):
    factor = Decimal(1 + percentage / 100)
    queryset.update(
        price=ExpressionWrapper(
            F('price') * factor,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )