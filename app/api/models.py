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

    def __init__(self):
        self.users = users

    def create_user(self, email, is_admin, password):
        """ create user method """

        user = {
            "user_id": len(users)+1,
            "email": email,
            "is_admin": is_admin,
            "password": password
        }

        self.users.append(user)
        return user

    # def get_all_users(self):
    #     """ get all users method """
    #     return users

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

    def __init__(self):
        self.products = products

    def create_product(self, product_name, category, quantity, unit_price):
        """ create product method """
        product = {
            "product_id": len(self.products)+1,
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "unit_price": unit_price,
        }
        self.products.append(product)
        return product

    def get_all_products(self):
        """ get all products method """
        return self.products

    def get_specific_product(self, product_id):
        """ get a specific product method """
        for product in self.products:
            if product['product_id'] == product_id:
                return product

    def update_product(self, product_name, category, quantity, unit_price):
        """ update a product method """
        product = {
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "unit_price": unit_price,
        }
        return product

    def delete_product(self, product_id):
        for product in self.products:
            if product['product_id'] == product_id:
                self.products.remove(product)
                return product


class Sale:
    """ Sale model """
    def __init__(self):
        self.sales = sales

    def get_unit_price(product_id):
        for product in products:
            if product['product_id'] == product_id:
                unit_price = product['unit_price']
                return unit_price

    def get_available_products(product_id):
        for product in products:
            if product['product_id'] == product_id:
                quantity = product['quantity']
                return quantity

    def make_sale(self, product_id, quantity):
        self.quantity = int(quantity)
        self.unit_price = Sale.get_unit_price(product_id)
        self.available_stock = Sale.get_available_products(product_id)

        remainder = self.available_stock-self.quantity
        for product in products:
            if product['product_id'] == product_id:
                if remainder >= 0:
                    product['quantity'] = remainder

        if self.available_stock >= self.quantity:

            sale = {
                "sale_id": len(self.sales)+1,
                "product_id": product_id,
                "quantity": self.quantity,
                "unit_price": self.unit_price,
                "cost": self.quantity * self.unit_price
            }
            self.sales.append(sale)

            return sale

    def get_all_sales(self):
        return self.sales

    def get_specific_sale(self, sale_id):
        for sale in self.sales:
            if sale['sale_id'] == sale_id:
                return sale