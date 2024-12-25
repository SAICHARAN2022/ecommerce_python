from django.core.management.base import BaseCommand
from faker import Faker
from products.models import products, category
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        faker = Faker()
        # Create Categories
        for _ in range(5):
            category.objects.create(name=faker.word())
        
        # Create Vendors and Products
        for _ in range(10):
            # vendor = User.objects.create_user(username=faker.user_name(), role='vendor', password='password')
            for _ in range(20):
                products.objects.create(
                    name=faker.word(),
                    description=faker.text(),
                    price=faker.random_int(min=100, max=5000),
                    stock=faker.random_int(min=1, max=100),
                    category=category.objects.order_by('?').first(),
                    # vendor=vendor
                )
