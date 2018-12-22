from flask import jsonify, request, make_response, Response
from flask_restful import Resource
from .models import *
from .validations import *
from functools import wraps
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    verify_jwt_in_request,
    get_jwt_claims,
    get_raw_jwt
)


def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        # if get_jwt_identity() != True:
        if claims['is_admin'] != True:
            return make_response(jsonify({"message": "Admin rights required!"}), 201)
            pass
        else:
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
        else:
            return fn(*args, **kwargs)
    return wrapper


class Register(Resource):
    """ User registration """

    def __init__(self):
        self.user = User()

    def post(self):
        data = request.get_json()
        try:
            # email = data['email']
            # is_admin = data['is_admin']
            # password = data['password']

            user_data = ValidateRegistration(
                data['email'], data['is_admin'], data['password'])
            user_data.validate()

            # user_data = ValidateRegistration(
            #     email, is_admin, password)
            # user_data.validate()

            new_user = self.user.create_user(
                email, is_admin, User.generate_hash(password))
            return make_response(jsonify({"message": "User {} was created".format(email), }), 201)
        except KeyError as error:
            return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)

    # def get(self):
    #     if len(users) > 0:
    #         return make_response(jsonify(self.user.get_all_users()), 200)
    #     else:
    #         return make_response(jsonify({'message': 'No user record(s) available'}), 200)


class Login(Resource):
    """ User login """

    def post(self):
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']
            user = User.search(email, password)
            if user:
                access_token = create_access_token(identity=user['is_admin'])
                return make_response(jsonify({
                    'message': 'Welcome {}'.format(email),
                    "access_token": access_token
                }))
            return make_response(jsonify({'message': 'wrong credentials'}), 200)
        except KeyError as error:
            return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)


class Logout(Resource):

    @jwt_required
    def post(self):
        revoked_tokens.append(get_raw_jwt()["jti"])
        return {"message": "Successfully logged out"}, 200
        # try:
            
        # except:
        #     return {"message": "Something went wrong"}, 500


class Products(Resource):
    """ admin and an attendant should be able to retrieve all products """

    def __init__(self):
        self.products = Product()

    @admin_required
    def post(self):
        """ Only admin can add a product """
        try:
            data = request.get_json()
            product_name = data['product_name']
            quantity = data['quantity']
            unit_price = data['unit_price']
            category = data['category']

            product_data = ValidateProduct(
                product_name, quantity, unit_price, category)
            product_data.validate()

            new_product = self.products.create_product(
                product_name, quantity, unit_price, category)
            return make_response(jsonify(new_product), 201)
        except KeyError as error:
            return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)

    @jwt_required
    def get(self):
        """ Admin/store attendant can get all products """
        if len(products) > 0:
            return make_response(jsonify({'message': 'Success','products': self.products.get_all_products()}), 200)
        else:
            return make_response(jsonify({'message': 'No product record(s) available'}), 200)


class GetSpecificProduct(Resource):
    """ Admin/store attendant can get a specific product """

    def __init__(self):
        self.products = Product()

    @jwt_required
    def get(self, product_id):
        product = self.products.get_specific_product(product_id)
        if product:
            return make_response(jsonify(product), 200)
        else:
            return make_response(jsonify({'message': 'Sorry, the product does not exist!'}), 404)


class UpdateProduct(Resource):
    """ Update a specific product """

    def __init__(self):
        self.products = Product()

    @jwt_required
    def put(self, product_id):
        product = self.products.get_specific_product(product_id)

        data = request.get_json()

        try:
            product_name = data['product_name']
            category = data['category']
            quantity = data['quantity']
            unit_price = data['unit_price']

            product_data = ValidateProduct(
                product_name, quantity, unit_price, category)
            product_data.validate()

            updated_product = self.products.update_product(
                product_name, quantity, unit_price, category)
        except KeyError as error:
            return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)

        return make_response(jsonify({'message': 'update successful!', 'product': updated_product}), 200)


class DeleteProduct(Resource):
    """ Delete a specific product """

    def __init__(self):
        self.product = Product()

    @admin_required
    def delete(self, product_id):
        if self.product.delete_product(product_id):
            return make_response(jsonify({'message': 'delete operation successful!'}), 200)
        else:
            return make_response(jsonify({'message': 'Sorry, the product does not exist!'}), 404)


class Sales(Resource):
    """ Show all sales """

    def __init__(self):
        self.sale = Sale()

    @attendant_required
    def post(self):
        try:
            data = request.get_json()
            product_id = data['product_id']
            quantity = data['quantity']

            sale_data = ValidateSale(product_id, quantity)
            sale_data.validate()

            if Sale.get_unit_price(product_id):
        # self.assertEqual(resp.status_code, 400)

                new_sale = self.sale.make_sale(product_id, quantity)

                if new_sale:
                    return make_response(jsonify(new_sale), 201)

                else:
                    return make_response(jsonify({'message': 'Insufficient stock'}), 200)
            else:
                return make_response(jsonify({'message': 'Warning! You are attempting to sale a non-existent product'}), 200)
        except KeyError as error:
            return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)

    @admin_required
    def get(self):
        if len(sales) > 0:
            return make_response(jsonify(self.sale.get_all_sales()), 200)
        else:
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
        else:
            return make_response(jsonify({'message': 'Sorry, sale record does not exist'}), 400)
