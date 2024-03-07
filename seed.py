from app import app, db
from models import Product
import random

def seed_products(category_name, product_list, min_products, max_products, descriptions=None, image_urls=None):
    with app.app_context():
        for _ in range(random.randint(min_products, max_products)):
            name = f"{category_name} - {random.choice(product_list)}"
            description = random.choice(descriptions) if descriptions else "One of the best products in our range."
            image_url = random.choice(image_urls) if image_urls else "https://via.placeholder.com/150"

            product = Product(
                name=name,
                description=description,
                image_url=image_url,
                price=random.randint(100, 1000),
                onstock=random.choice([True, False]),
                rating=random.randint(1, 5)
            )
            db.session.add(product)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Seed data
        categories = {
            "Shirts": {
                "product_list": ['Classic', 'Slim Fit', 'Oxford'],
                "min_products": 5,
                "max_products": 10,
                "descriptions": ['Stylish and comfortable', 'High-quality fabric', 'Perfect for casual wear'],
                "image_urls": [
                    'https://example.com/shirt1.jpg',
                    'https://example.com/shirt2.jpg'
                ]
            },
            # Add other categories similarly...
        }

        for category, details in categories.items():
            seed_products(category, **details)

        print("Database seeding complete.")
