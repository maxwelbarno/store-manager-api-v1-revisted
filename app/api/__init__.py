from flask import Blueprint
from flask_restful import Api
from .views import *


# create blueprint
v1_blueprint = Blueprint('api_v1', __name__, url_prefix="/api/v1")
api_v1 = Api(v1_blueprint)

# create endpoints
api_v1.add_resource(Register, '/register')
api_v1.add_resource(Login, '/login')
api_v1.add_resource(Logout, '/logout')
api_v1.add_resource(Products, '/products')
api_v1.add_resource(GetSpecificProduct, '/products/<int:product_id>')
api_v1.add_resource(UpdateProduct, '/products/<int:product_id>')
api_v1.add_resource(DeleteProduct, '/products/<int:product_id>')
api_v1.add_resource(Sales, '/sales')
api_v1.add_resource(GetSpecificSale, '/sales/<int:sale_id>')
