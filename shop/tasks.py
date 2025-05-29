# tasks.py
from celery import chain, shared_task
from .models import Product
import csv
from django.core.mail import send_mail

@shared_task
def import_csv_data():
    with open('mock_products.csv') as f:
        return list(csv.DictReader(f))

@shared_task
def validate_and_update(data):
    report = []
    for row in data:
        sku = row.get('sku')
        quantity = int(row.get('quantity', 0))
        product, _ = Product.objects.update_or_create(
            sku=sku,
            defaults={'quantity': quantity}
        )
        report.append(f'{sku}: {quantity}')
    return report

@shared_task
def send_report(report):
    message = '\n'.join(report)
    # send_mail('Inventory Report', message, 'noreply@example.com', ['admin@example.com'])

# run it using celery -A shop.tasks.nightly_task_chain or direct from terminal
def nightly_task_chain():
    chain(import_csv_data.s(), validate_and_update.s(), send_report.s())()
