from flask import abort
from .models import *
import re


# class ValidateRegistration:
#     """ User registration details validations """

#     def __init__(self, email, is_admin, password):
#         self.email = email
#         self.is_admin = is_admin
#         self.password = password

def validate(email, is_admin, password):
    email = email
    is_admin = is_admin
    password = password
    if email == "" or is_admin == "" or password == "":
        message = "Sorry, there's an empty user value, please check your input values"
        abort(400, message)

    for user in users:
        if email == user['email']:
            message = "That email is already registered, please login!"
            abort(400, message)

    if not re.match("^[a-zA-Z0-9!#$&_*?^{}~-]+(\.[a-zA-Z0-9!#$&_*?^{}~-]+)*@([a-z0-9]+([a-z0-9-]*)\.)+[a-zA-Z]+$", email):
        message = "Please use a valid email address"
        abort(400, message)

    if re.match("^[a-zA-Z0-9!#$&_*?^{}~-]+(\.[a-zA-Z0-9!#$&_*?^{}~-]+)*@([a-z0-9]+([a-z0-9-]*)\.)+[a-zA-Z]+$", email) and type(is_admin) != bool:
        message = "is_admin value must be a boolean!"
        abort(400, message)

    if len(password) < 6:
        message = "password is too short, it should be more than 6 characters!"
        abort(400, message)


# class ValidateLogin:
#     """ User login validation """

#     def __init__(self, email, password):
#         self.email = email,
#         self.password = password

#     def validate(self):
#         if self.email == "" or self.password == "":
#             message = "Sorry, there's an empty user value, please check your input values"
#             abort(400, message)
#         if type(self.email) != str:
#             message = "An email adress value must be a string"
#             abort(400, message)

#         if not re.match("^[a-zA-Z0-9!#$&_*?^{}~-]+(\.[a-zA-Z0-9!#$&_*?^{}~-]+)*@([a-z0-9]+([a-z0-9-]*)\.)+[a-zA-Z]+$", self.email):
#             message = "Use a valid email address"
#             abort(400, message)

#         if type(self.password) != str:
#             message = "An  value must be a string"
#             abort(400, message)


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
                message = "Sorry, such a product already exists, please confirm its category"
                abort(400, message)

        if self.product_name == "" or self.quantity == "" or self.unit_price == "" or self.category == "":
            message = "Sorry, there's an empty value, please check your input values"
            abort(400, message)

        if type(self.product_name) != str:
            message = "A product name's value must be a string"
            abort(400, message)

        if type(self.category) != str:
            message = "A category's value must be a string"
            abort(400, message)

        if type(self.quantity) != int:
            message = "A quantity's value must be an integer"
            abort(400, message)

        if self.quantity <= 0:
            message = "A quantity's value must be a positive integer"
            abort(400, message)

        if type(self.unit_price) != float:
            message = "A price's value must be of float data type"
            abort(400, message)

        if self.unit_price <= 0:
            message = "A price's value must be a positive float"
            abort(400, message)


class ValidateSale:
    """ Sale validation """

    # if len(users) > 0:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    def validate(self):
        # for sale in sales:
        if self.product_id == "" or self.quantity == "":
            message = "Sorry, there's an empty value, please check your input values"
            abort(400, message)
        if type(self.product_id) != int:
            message = "A sale id's value must be an int"
            abort(400, message)

        if type(self.quantity) != int:
            message = "A quantity's value must be an integer"
            abort(400, message)

        if self.quantity <= 0:
            message = "quantity cannot be less than one"
            abort(400, message)
