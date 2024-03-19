from app import app, db
from models import Product, User, Wishlist
import random

def seed_products(category_name, product_list, min_products, max_products, descriptions=None, image_urls=None):
    with app.app_context():
        categoriess = ["Shirts", "Trousers", "Suits", "Shoes", "Curtains", "Duvets", "Carpets", "Towels"]
        for _ in range(random.randint(min_products, max_products)):
            name = f"{category_name} - {random.choice(product_list)}"
            description = random.choice(descriptions) if descriptions else "One of the best products in our range."
            image_url = random.choice(image_urls) if image_urls else "https://via.placeholder.com/150"

            product = Product(
                name=name,
                description=description,
                image_url=image_url,
                price=random.randint(100, 1000),
                onstock=True,
                rating=random.randint(1, 5),
                category=random.choice(categoriess)
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
                "image_urls":[
                    'https://images.pexels.com/photos/769749/pexels-photo-769749.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/1232459/pexels-photo-1232459.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/1337477/pexels-photo-1337477.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/356252/pexels-photo-356252.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/3764571/pexels-photo-3764571.jpeg?auto=compress&cs=tinysrgb&w=600'
                ]
            },
            "Trousers": {
                "product_list": ['trouser'],
                "min_products": 5,
                "max_products": 10,
                "descriptions": ['Sturdy and durable', 'Cool for summer', 'Elegant and stylish'],
                "image_urls":  [
                    'https://images.pexels.com/photos/3764571/pexels-photo-3764571.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/346749/pexels-photo-346749.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/914668/pexels-photo-914668.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/15984043/pexels-photo-15984043.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/15860723/pexels-photo-15860723.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/15984000/pexels-photo-15984000.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/7764611/pexels-photo-7764611.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/6975488/pexels-photo-6975488.jpeg?auto=compress&cs=tinysrgb&w=600'
                ]
            },
            "Suits": {
                "product_list": ['suit'],
                "min_products": 5,
                "max_products": 10,
                "descriptions": ['Soft and absorbent', 'Elegant design', 'Durable material'],
                "image_urls": [
                    'https://images.pexels.com/photos/9834550/pexels-photo-9834550.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/7691251/pexels-photo-7691251.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/2005356/pexels-photo-2005356.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/14559459/pexels-photo-14559459.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/157675/pexels-photo-157675.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/7691068/pexels-photo-7691068.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/2709563/pexels-photo-2709563.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/9155710/pexels-photo-9155710.jpeg?auto=compress&cs=tinysrgb&w=600'
                ]
            },
            "Shoes": {
                "product_list": ['shoe'],
                "min_products": 5,
                "max_products": 10,
                "descriptions": ['Sporty and comfortable', 'Sturdy and durable', 'Elegant and stylish'],
                "image_urls":  [
                    'https://www.pexels.com/photo/man-wearing-black-leather-boots-5214139/',
                    'https://www.pexels.com/photo/nike-shoes-on-black-backround-1598505/',
                    'https://www.pexels.com/photo/focus-photography-of-pair-of-red-nike-running-shoes-1027130/',
                    'https://www.pexels.com/photo/photo-of-pair-of-vans-sneakers-1598508/',
                    'https://images.pexels.com/photos/1335463/pexels-photo-1335463.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://www.pexels.com/photo/unpaired-yellow-dr-martens-lace-up-boot-1159670/',
                    'https://www.pexels.com/photo/selective-focus-photography-of-white-nike-air-force-1-low-2048548/',
                    'https://www.pexels.com/photo/pair-of-brown-leather-casual-shoes-on-table-298863/',
                    'https://www.pexels.com/photo/person-wearing-white-slides-slippers-8250260/',
                    'https://www.pexels.com/photo/soda-in-can-beside-the-smartphone-14650679/',
                    'https://www.pexels.com/photo/black-and-white-slides-on-the-floor-14313221/',
                    'https://www.pexels.com/photo/a-person-wearing-a-slides-on-the-beach-sand-6654353/'
                ]
            },
            "Curtains": {
                "product_list": ['curtain'],
                "min_products": 5,
                "max_products": 10,
                "descriptions": ['Soft and elegant', 'Durable material'],
                "image_urls":  [
                    'https://images.pexels.com/photos/1571450/pexels-photo-1571450.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/2380247/pexels-photo-2380247.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/969593/pexels-photo-969593.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/3034738/pexels-photo-3034738.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/265795/pexels-photo-265795.jpeg?auto=compress&cs=tinysrgb&w=600'
                ]
            },
            "Duvets": {
                "product_list": ['duvet'],
                "min_products": 5,
                "max_products": 10,
                "descriptions": ['Warm and cozy', 'Elegant design'],
                "image_urls": [
                    'https://images.pexels.com/photos/8416216/pexels-photo-8416216.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/6316054/pexels-photo-6316054.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/4940710/pexels-photo-4940710.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/7018391/pexels-photo-7018391.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/6045221/pexels-photo-6045221.jpeg?auto=compress&cs=tinysrgb&w=600'
                ]
            },
            "Carpets": {
                "product_list": ['carpet'],
                "min_products": 5,
                "max_products": 10,
                "descriptions": ['Soft and comfortable', 'Stylish design'],
                "image_urls":  [
                    'https://images.pexels.com/photos/2580426/pexels-photo-2580426.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/447592/pexels-photo-447592.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/10651202/pexels-photo-10651202.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/17527834/pexels-photo-17527834.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/15865416/pexels-photo-15865416.jpeg?auto=compress&cs=tinysrgb&w=600'
                ]
            },
            "Towels": {
                "product_list": ['towel'],
                "min_products": 5,
                "max_products": 10,
                "descriptions": ['Absorbent and soft', 'Durable material'],
                "image_urls": [
                    'https://images.pexels.com/photos/12679/pexels-photo-12679.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/2672634/pexels-photo-2672634.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/1624753/pexels-photo-1624753.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/4210314/pexels-photo-4210314.jpeg?auto=compress&cs=tinysrgb&w=600',
                    'https://images.pexels.com/photos/8301493/pexels-photo-8301493.jpeg?auto=compress&cs=tinysrgb&w=600'
                ]
            }
        }

        for category, details in categories.items():
            seed_products(category, **details)

        print("Database seeding complete.")   
