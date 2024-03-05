
from app import app, db
from models import Product
import random 
from sqlalchemy import func 

def seed_products(product_name, product_list, min_products, max_products, descriptions=None):
    product =  Product(name=product_name)
    db.session.add(product)
    db.session.commit()

    num_products = random.randint(min_products, max_products)
    for _ in range(20):
        product_name = random.choice(product_list)
        description = random.choice(descriptions) if descriptions else "No description available"
        product = Product(name=product_name, product_id=product.id, description=description)
        db.session.add(product)
    db.session.commit()

with app.app_context():
    # Delete existing data
    Product.query.delete()
    
    clothes = ['dress ', 'trouser', 'shirt ','jacket' ,'shorts' ,'jacket','polloshirt','gymsuites','jeans'] 
    clothes_description = ['stylish and comfortable', 'High-quality fabric','casualwear']
    clothes_prices = [300,400,600,100,400,900,1500,2000,2500,900,3000,4000,1600,1900]
    seed_products("Clothes",clothes ,20,35,clothes_prices,clothes_description)

     
    shoes = ['sneakers', 'boots', 'sandals', 'heels', 'loafers']
    shoe_descriptions = ['Sporty and comfortable', 'Sturdy and durable', 'Cool for summer', 'Elegant and stylish', 'Casual and versatile']
    shoe_prices = [700, 1200, 500, 1000, 800]
    seed_products("Shoes",shoes, 12,15 ,shoe_prices,shoe_descriptions)

    house_hold_items = ['curtain', 'duvet', 'towels', 'carpet', 'pillowcase']
    house_hold_descriptions = ['Soft and absorbent', 'Elegant design', 'Durable material']
    house_hold_price =[1500,600,800,400,300,2000,1000,700]
    seed_products("Household Items", house_hold_items, 10, 12,house_hold_price, house_hold_descriptions)

 
    electronics = ['phones', 'laptops', 'charger', 'powerbank', 'external cables', 'microwave', 'oven', 'dishwasher', 'washing machine', 'blowdry']
    electronics_descriptions = ['High-performance', 'Energy-efficient', 'Sleek and modern design']
    seed_products("Electronics", electronics, 9, 12, electronics_descriptions)




