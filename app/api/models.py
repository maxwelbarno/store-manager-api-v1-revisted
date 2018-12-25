# import password encryption module
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

# lists
products = [{
    "product_id": 1,
    "product_name": "mocha coffee",
    "category": "beverages",
    "quantity": 100,
    "unit_price": 200.00
},
    {
    "product_id": 2,
    "product_name": "capuccino coffee",
    "category": "beverages",
    "quantity": 200,
    "unit_price": 250.00
}]
sales = [{
    "cost": 1000,
    "product_id": 1,
    "quantity": 1,
    "sale_id": 1,
    "unit_price": 200
},
    {
    "cost": 800,
    "product_id": 2,
    "quantity": 5,
    "sale_id": 2,
    "unit_price": 140
}]
users = []
revoked_tokens = []


class User:
    """ User model """

    def create_user(email, is_admin, password):
        """ create user method """

        user = {
            "user_id": len(users)+1,
            "email": email,
            "is_admin": is_admin,
            "password": password
        }

        users.append(user)
        return user

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
    
    def search(email, password): 
        for user in users: 
            if user['email'] == email and User.verify_hash(password, user['password']):
                return user


class Product:
    """ Product model """

    def create_product(product_name, category, quantity, unit_price):
        """ create product method """
        product = {
            "product_id": len(products)+1,
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "unit_price": unit_price,
        }
        products.append(product)
        return product

    def get_all_products():
        """ get all products method """
        return products
        

    def get_specific_product(product_id):
        """ get a specific product method """
        for product in products:
            if product['product_id'] == product_id:
                return product

    def update_product(product_name, category, quantity, unit_price):
        """ update a product method """
        product = {
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "unit_price": unit_price,
        }
        return product

    def delete_product(product_id):
        for product in products:
            if product['product_id'] == product_id:
                products.remove(product)
                return product


class Sale:
    """ Sale model """
    def __init__(self):
        self.sales = sales

    # def get_product(product_id):
    #     for product in products:
    #         if product['product_id'] == product_id:
    #             return product

    def make_sale(product_id, quantity):
        """ sale an item """
        quantity = int(quantity)
        price = Sale.get_price(product_id)
        available_stock = Sale.get_quantity(product_id)

        remainder = available_stock-quantity
        for product in products:
            if product['product_id'] == product_id:
                if remainder >= 0:
                    product['quantity'] = remainder

        if available_stock >= quantity:

            sale = {
                "sale_id": len(sales)+1,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": price,
                "cost": quantity * price
            }
            sales.append(sale)

            return sale

    def get_all_sales():
        """ Get all sales """
        return sales

    def get_specific_sale(self, sale_id):
        """ Get specific sale item """
        for sale in self.sales:
            if sale['sale_id'] == sale_id:
                return sale

    def get_price(product_id):
        """ Get price of the item"""
        for product in products:
            if product['product_id'] == product_id:
                unit_price = product['unit_price']
                return unit_price

    def get_quantity(product_id):
        """ Get available quantity of the item"""
        for product in products:
            if product['product_id'] == product_id:
                quantity = product['quantity']
                return quantity