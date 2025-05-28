# Ecommerce Inventory Management

A Django-based ecommerce backend with REST API, Celery task queue, Redis, and webhook integration for inventory management.

---

## Features

- **Product CRUD API**: Manage products with fields like name, SKU, price, quantity, and last updated timestamp.
- **Filtering & Searching**: Filter products by price, SKU, name, and quantity.
- **Authentication**: Basic auth restricting API access to authorized users.
- **Webhook Endpoint**: Handles Shopify inventory update webhooks.
- **Admin Interface**: Advanced filtering and bulk price update actions.
- **Nightly Background Tasks**: Celery task chain that:
  1. Imports product data from a CSV.
  2. Validates and updates inventory.
  3. Sends inventory update reports via email.
- **Database Integrity**: Uses transactions for safe updates.
- **Testing**: Basic unit tests for API, webhook, and Celery tasks.
- **Dockerized**: Easy setup with Docker Compose using Redis as broker/backend.

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.8+
- (Optional) Redis CLI to interact with Redis

---

### Setup Instructions

1. **Clone repository**

```bash
git clone https://github.com/yourusername/ecommerce-inventory.git
cd ecommerce-inventory
````


2. **Docker Setup**

```bash
docker compose up --build
```


Code Review Checklist:

- ✅ API endpoints follow RESTful conventions.
- ✅ Proper use of HTTP status codes and error handling.
- ✅ Clear and concise docstrings and comments throughout the code.
- ✅ Use of appropriate Django views and serializers.
- ✅ Tests are written for views, models, and Celery tasks to ensure coverage and stability.
- ✅ Database queries are optimized and use transactions where necessary.
- ✅ Adherence to Django best practices
- ✅ Secure API access with authentication and permission checks.
- ✅ Code is modular and easy to maintain or extend.
- ✅Dont work direclty on main branch create branch and then MR

Onboarding Plan:

Day 1–2: Setup environment using README.md, run test suite.

Day 3: Review existing models and APIs.

Day 4–5: Assign first small bug fix or task.

Week 2: Pair programming and write a new endpoint.

Ongoing: Code review.

