from app import app, db
from models import Product, User, Wishlist
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
                "image_urls":[
    'https://www.pexels.com/photo/man-in-white-shirt-beige-baseball-cap-and-sunglasses-sitting-in-a-street-cafe-18393494/',
    'https://www.pexels.com/photo/photo-of-man-wearing-headphones-2954389/',
    'https://www.pexels.com/photo/man-in-white-and-blue-plaid-dress-shirt-769749/',
    'https://www.pexels.com/photo/man-wearing-blue-lacoste-polo-shirt-and-silver-colored-analog-watch-1232459/',
    'https://www.pexels.com/photo/man-holding-jacket-1337477/',
    'https://www.pexels.com/photo/white-cigarette-stick-356252/',
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
        'https://www.pexels.com/photo/woman-wearing-distressed-blue-jeans-holding-paper-bags-346749/',
        'https://www.pexels.com/photo/woman-in-gray-blazer-stands-on-gray-concrete-floor-914668/',
        'https://www.pexels.com/photo/smiling-model-in-black-blouse-and-pants-15984043/',
        'https://www.pexels.com/photo/man-in-black-dancing-on-steps-15860723/',
        'https://www.pexels.com/photo/elegant-woman-eating-pastry-at-cafe-15984000/',
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
        'https://www.pexels.com/photo/a-group-of-women-standing-on-the-rock-while-wearing-blazers-and-pants-9834550/',
        'https://images.pexels.com/photos/7691251/pexels-photo-7691251.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://images.pexels.com/photos/2005356/pexels-photo-2005356.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://www.pexels.com/photo/elegant-woman-in-a-beige-suit-posing-on-sand-14559459/',
        'https://www.pexels.com/photo/man-wearing-black-hat-and-black-coat-157675/',
        'https://www.pexels.com/photo/stylish-women-in-suits-in-studio-7691068/',
        'https://images.pexels.com/photos/2709563/pexels-photo-2709563.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://www.pexels.com/photo/woman-in-green-suit-looking-at-man-in-white-jacket-9155710/'
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
        'https://www.pexels.com/photo/two-white-rod-pocket-curtains-910458/',
        'https://www.pexels.com/photo/photograph-of-bedroom-interior-1571450/',
        'https://www.pexels.com/photo/brown-and-gray-armchair-near-window-2380247/',
        'https://www.pexels.com/photo/gray-window-curtains-969593/',
        'https://www.pexels.com/photo/orange-window-curtain-3034738/',
        'https://www.pexels.com/photo/gray-padded-chairs-with-wooden-bases-aligned-beside-table-near-window-265795/'
    ]

        },
        "Duvets": {
            "product_list": ['duvet'],
            "min_products": 5,
            "max_products": 10,

            "descriptions": ['Warm and cozy', 'Elegant design'],
            "image_urls": [
        'https://www.pexels.com/photo/young-people-wrapped-in-quilts-sleeping-standing-up-8416216/',
        'https://www.pexels.com/photo/made-bed-in-spacious-bedroom-with-air-conditioner-6316054/',
        'https://www.pexels.com/photo/interior-of-classic-styled-room-with-comfortable-bed-and-table-lamp-4940710/',
        'https://www.pexels.com/photo/stylish-bedroom-interior-with-comfortable-bed-and-vanity-table-7018391/',
        'https://www.pexels.com/photo/mattress-in-bedroom-at-home-6045221/'
    ]

        },
        "Carpets": {
            "product_list": ['carpet'],
            "min_products": 5,
            "max_products": 10,

            "descriptions": ['Soft and comfortable', 'Stylish design'],
            "image_urls":  [
        'https://www.pexels.com/photo/staircase-2580426/',
        'https://www.pexels.com/photo/round-beige-and-brown-wooden-table-and-chair-447592/',
        'https://www.pexels.com/photo/couple-standing-by-fence-in-countryside-10651202/',
        'https://www.pexels.com/photo/men-in-traditional-clothing-sitting-and-praying-17527834/',
        'https://www.pexels.com/photo/newlyweds-posing-in-park-15865416/'
    ]

        },
        "Towels": {
            "product_list": ['towel'],
            "min_products": 5,
            "max_products": 10,
            "descriptions": ['Absorbent and soft', 'Durable material'],
            "image_urls": [
        'https://www.pexels.com/photo/white-towel-12679/',
        'https://images.pexels.com/photos/2672634/pexels-photo-2672634.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://www.pexels.com/photo/brown-classical-guitar-on-blue-towel-1624753/',
        'https://images.pexels.com/photos/4210314/pexels-photo-4210314.jpeg?auto=compress&cs=tinysrgb&w=600',
        'https://www.pexels.com/photo/girl-in-blue-and-white-towel-standing-on-brown-sand-near-the-beach-8301493/'
]

        }
            
            }

        for category, details in categories.items():
            seed_products(category, **details)

        print("Database seeding complete.")     


    
    
