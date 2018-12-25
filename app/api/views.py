from flask import jsonify, request, make_response, Response
from flask_restful import Resource
from .models import *
from .validations import *
from functools import wraps
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, verify_jwt_in_request, get_jwt_claims, get_raw_jwt)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['is_admin'] != True:
            return make_response(jsonify({"message": "Admin rights required!"}), 201)
            pass
        return fn(*args, **kwargs)
    return wrapper

def attendant_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['is_admin'] != False:
            return make_response(jsonify({"message": "Attendant rights required!"}), 201)
            pass
        return fn(*args, **kwargs)
    return wrapper

def user(email, is_admin, password):
    """ custom create user function """
    email=email
    is_admin=is_admin
    password=password
    ValidateRegistration.validate(email, is_admin, password)
    new = User.create_user(email, is_admin, User.generate_hash(password))
    return True

def product_validation(product_name, category, quantity, price):
    """ custom product validation """
    product_name = product_name
    category=category
    quantity=quantity
    price=price
    validated_product=ValidateProduct.validate(product_name, category, quantity, price)
    return validated_product

def product_create(product_name, category, quantity, price):
    """ custom create product function """
    product_validation(product_name, category, quantity, price)
    return Product.create_product(product_name, category, quantity, price)

def product_update(product_name, category, quantity, price):
    """ custom product update function """
    product_validation(product_name, category, quantity, price)
    return Product.update_product(product_name, category, quantity, price)

def validate_sale(product_id, quantity):
    return ValidateSale.validate(product_id, quantity)

def error_handling(error):
    """ key error handling """
    error = error
    return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)


class Register(Resource):
    """ User registration """

    def post(self):
        data = request.get_json()
        try:
            user(data['email'], data['is_admin'], data['password'])
            return make_response(jsonify({"message": "User {} was created".format(data['email']), }), 201)
        except KeyError as error:
            return error_handling(error)


class Login(Resource):
    """ User login """

    def post(self):
        try:
            data = request.get_json()
            user = User.search(data['email'], data['password'])
            if user:
                access_token = create_access_token(identity=user['is_admin'])
                return make_response(jsonify({
                    'message': 'Welcome {}'.format(data['email']),
                    "access_token": access_token
                }))
            return make_response(jsonify({'message': 'wrong credentials'}), 200)
        except KeyError as error:
            return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)


class Logout(Resource):

    @jwt_required
    def post(self):
        revoked_tokens.append(get_raw_jwt()["jti"])
        return make_response(jsonify({'message': 'Successfully logged out'}), 200)


class Products(Resource):
    """ admin and an attendant should be able to retrieve all products """
    
    @admin_required
    def post(self):
        """ Only admin can add a product """
        try:
            data = request.get_json()
            product_create(data['product_name'], data['category'], data['quantity'], data['unit_price'])
            return make_response(jsonify(), 201)
        except KeyError as error:
            return error_handling(error)

    @jwt_required
    def get(self):
        """ Admin/store attendant can get all products """
        if len(products) > 0:
            return make_response(jsonify({'message': 'Success','products': Product.get_all_products()}), 200)
        return make_response(jsonify({'message': 'No product record(s) available'}), 200)


class GetSpecificProduct(Resource):

    @jwt_required
    def get(self, product_id):
        product = Product.get_specific_product(product_id)
        if product:
            return make_response(jsonify(product), 200)
        return make_response(jsonify({'message': 'Sorry, the product does not exist!'}), 404)


class UpdateProduct(Resource):
    """ Update a specific product """

    @jwt_required
    def put(self, product_id):
        Product.get_specific_product(product_id)
        data = request.get_json()
        try:
            product= product_update(data['product_name'], data['category'], data['quantity'], data['unit_price'])
            return make_response(jsonify({'message': 'update successful!', 'product': product}), 201)
        except KeyError as error:
            return error_handling(error)


class DeleteProduct(Resource):
    """ Delete a specific product """

    @admin_required
    def delete(self, product_id):
        if Product.delete_product(product_id):
            return make_response(jsonify({'message': 'delete operation successful!'}), 200)
        return make_response(jsonify({'message': 'Sorry, the product does not exist!'}), 404)


class Sales(Resource):
    """ Show all sales """

    def __init__(self):
        self.sale = Sale()

    @attendant_required
    def post(self):
        try:
            data = request.get_json()
            validate_sale(data['product_id'], data['quantity'])

            if Product.get_specific_product(data['product_id']):
                new_sale = self.sale.make_sale(data['product_id'], data['quantity'])
                if new_sale:
                    return make_response(jsonify(new_sale), 201)
                return make_response(jsonify({'message': 'Insufficient stock'}), 200)
            return make_response(jsonify({'message': 'Warning! You are attempting to sale a non-existent product'}), 200)
        except KeyError as error:
            return error_handling(error)

    @admin_required
    def get(self):
        if len(sales) > 0:
            return make_response(jsonify(self.sale.get_all_sales()), 200)
        return make_response(jsonify({'message': 'No sale record(s) available'}), 200)


class GetSpecificSale(Resource):
    """ An attendant should be able to retrieve a specific sale item """

    def __init__(self):
        self.sale = Sale()

    @attendant_required
    def get(self, sale_id):
        sale = self.sale.get_specific_sale(sale_id)
        if sale:
            return make_response(jsonify({'message': 'Success','sale': sale}), 200)
        return make_response(jsonify({'message': 'Sorry, sale record does not exist'}), 400)
