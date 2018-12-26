from flask import abort
from .models import *
import re

def error(message):
    return abort(400, message)

def user_values_contain_blanks(email, is_admin, password):
    email=email
    is_admin=is_admin
    password=password
    if email == "" or is_admin == "" or password == "":
        return True

def user_exists(email):
    email = email
    for user in users:
        if email == user['email']:
            return True

def invalid_email(email):
    email = email
    if not re.match("^[a-zA-Z0-9!#$&_*?^{}~-]+(\.[a-zA-Z0-9!#$&_*?^{}~-]+)*@([a-z0-9]+([a-z0-9-]*)\.)+[a-zA-Z]+$", email):
        return True

def pasword_is_short(password):
    password=password
    if len(password) < 6:
        return True

def is_admin_value_not_boolean(email, is_admin):
    email=email
    is_admin=is_admin
    if not invalid_email(email) and type(is_admin) != bool:
        return True

def product_exists(product_name, category, quantity, price):
    product_name = product_name
    category = category
    quantity = quantity
    price = price
    if check_product(product_name, category) and correct_types(quantity, price):
        return True

def product_values_contain_blanks(product_name, category, quantity, price):
    product_name = product_name
    category = category
    quantity = quantity
    price = price
    if product_name == "" or quantity == "" or price == "" or category == "":
        return True

def check_product(product_name, category):
    category=category
    product_name = product_name
    for product in products:
        if product_name == product['product_name'] and category == product['category']:
            return True


def correct_types(quantity, price):
    quantity=quantity
    price=price
    if not non_int_quantity(quantity) and not non_float_price(price) and not sub_zero_price(price) and not sub_zero_quantity(quantity):
        return True

# def positive_values(quantity, price):
#     quantity=quantity
#     price=price
#     if not sub_zero_price(price) and not sub_zero_quantity(quantity):
#         return True


def non_string_product_name(product_name):
    product=product_name
    if type(product_name) != str:
        return True

def non_string_category(category):
    category=category
    if type(category) != str:
        return True

def non_int_quantity(quantity):
    quantity=quantity
    if type(quantity) != int:
        return True

def sub_zero_quantity(quantity):
    quantity=quantity
    if quantity <= 0:
        return True

def non_float_price(price):
    price=price
    if type(price) != float:
        return True

def sub_zero_price(price):
    price=price
    if price < 0 :
        return True

def non_int_product_id(product_id):
    product_id=product_id
    if type(product_id) != int:
        return True

def sale_values_contain_blanks(product_id, quantity):
    product_id = product_id
    quantity = quantity
    if product_id == "" or quantity == "":
        return True

class ValidateRegistration:
    """ User registration details validations """

    def validate(email, is_admin, password):
        """ validate sale """
        email=email
        is_admin=is_admin
        password=password

        if user_values_contain_blanks(email, is_admin, password):
            error("Sorry, there's an empty user value, please check your input values")

        if user_exists(email):
            error("That email is already registered, please login!")

        if invalid_email(email):
            error("Please use a valid email address")

        if is_admin_value_not_boolean(email, is_admin):
            error("is_admin value must be a boolean!")

        if pasword_is_short(password):
            error("password is too short, it should be more than 6 characters!")


class ValidateProduct:
    """ Product details validations """

    def validate(product_name, category, quantity, unit_price):
        """ validate product """
        product_name=product_name
        category=category
        quantity=quantity
        unit_price=unit_price

        if product_exists(product_name, category, quantity, unit_price):
            error("Sorry, such a product already exists, please confirm its category")

        if product_values_contain_blanks(product_name, category, quantity, unit_price):
            error("Sorry, there's an empty value, please check your input values")

        if non_string_product_name(product_name):
            error("A product name's value must be a string")

        if non_string_category(category):
            error("A category's value must be a string")

        if non_int_quantity(quantity):
            error("A quantity's value must be an integer")
        
        if sub_zero_quantity(quantity):
            error("A quantity's value must be a positive integer")

        if non_float_price(unit_price):
            error("A price's value must be of float data type")

        if sub_zero_price(unit_price):
            error("A price's value must be a positive float")


class ValidateSale:
    """ Sale validation """

    def validate(product_id, quantity):
        """ validate sale """
        product_id = product_id
        quantity = quantity

        if sale_values_contain_blanks(product_id, quantity):
            error("Sorry, there's an empty value, please check your input values")

        if non_int_product_id(product_id):
            error("A sale id's value must be an int")

        if non_int_quantity(quantity):
            error("A quantity's value must be an integer")

        if sub_zero_quantity(quantity):
            error("A quantity's value must be a positive integer")
