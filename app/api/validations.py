from flask import abort
from .models import *
import re

def error(message):
    return abort(400, message)

def blanks(email, is_admin, password):
    email=email
    is_admin=is_admin
    password=password
    if email == "" or is_admin == "" or password == "":
        return True
    # email=""
    # is_admin=""
    # password=""




class ValidateRegistration:
    """ User registration details validations """

    def __init__(self, email, is_admin, password):
        self.email = email
        self.is_admin = is_admin
        self.password = password

    def validate(self):
        if blanks(self.email, self.is_admin, self.password):
        # if self.email == "" or self.is_admin == "" or self.password == "":
            error("Sorry, there's an empty user value, please check your input values")

        for user in users:
            if self.email == user['email']:
                error("That email is already registered, please login!")

        if not re.match("^[a-zA-Z0-9!#$&_*?^{}~-]+(\.[a-zA-Z0-9!#$&_*?^{}~-]+)*@([a-z0-9]+([a-z0-9-]*)\.)+[a-zA-Z]+$", self.email):
            error("Please use a valid email address")

        if re.match("^[a-zA-Z0-9!#$&_*?^{}~-]+(\.[a-zA-Z0-9!#$&_*?^{}~-]+)*@([a-z0-9]+([a-z0-9-]*)\.)+[a-zA-Z]+$", self.email) and type(self.is_admin) != bool:
            error("is_admin value must be a boolean!")

        if len(self.password) < 6:
            error("password is too short, it should be more than 6 characters!")


class ValidateProduct:
    """ Product details validations """

    def __init__(self, product_name, quantity, unit_price, category):
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.category = category

    def validate(self):
        for product in products:
            if self.product_name == product['product_name'] and self.category == product['category'] and type(self.quantity) == int and type(self.unit_price) == float and self.quantity >= 0 and self.unit_price >= 0:
                error("Sorry, such a product already exists, please confirm its category")

        if self.product_name == "" or self.quantity == "" or self.unit_price == "" or self.category == "":
            error("Sorry, there's an empty value, please check your input values")

        if type(self.product_name) != str:
            error("A product name's value must be a string")

        if type(self.category) != str:
            error("A category's value must be a string")

        if type(self.quantity) != int:
            error("A quantity's value must be an integer")

        if self.quantity <= 0:
            error("A quantity's value must be a positive integer")

        if type(self.unit_price) != float:
            error("A price's value must be of float data type")

        if self.unit_price <= 0:
            error("A price's value must be a positive float")


class ValidateSale:
    """ Sale validation """

    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    def validate(self):
        if self.product_id == "" or self.quantity == "":
            error("Sorry, there's an empty value, please check your input values")
            
        if type(self.product_id) != int:
            error("A sale id's value must be an int")

        if type(self.quantity) != int:
            error("A quantity's value must be an integer")

        if self.quantity <= 0:
            error("quantity cannot be less than one")
