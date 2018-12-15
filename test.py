import unittest
import os
import json
from app import create_app
from flask import current_app
from app.api.models import users, products;

class ProductTestCase(unittest.TestCase):
    """ This class represents the product test case """

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

        self.test_admin_user = json.dumps(dict(
            email='test@test.com',
            is_admin=True,
            password="test123"
        ))

        self.test_attendant_user = json.dumps(dict(
            email='tests@test.com',
            is_admin=False,
            password="test123"
        ))

        self.test_blank_value_user = json.dumps(dict(
            email='',
            is_admin=True,
            password="test123"
        ))

        self.test_invalid_email_user = json.dumps(dict(
            email='test',
            is_admin=True,
            password="test123"
        ))

        self.test_non_boolean_is_admin_value_user = json.dumps(dict(
            email='tests@test.com',
            is_admin="true",
            password="test123"
        ))

        self.test_short_password = json.dumps(dict(
            email='testy@test.com',
            is_admin=True,
            password="test"
        ))

        self.user_login = json.dumps(dict(
            email='test@test.com',
            password="test123"
        ))

        self.attendant_user_login = json.dumps(dict(
            email='tests@test.com',
            password="test123"
        ))

        self.product = json.dumps(dict(
            product_id=1,
            category='beverages',
            product_name='coffee',
            quantity=100,
            unit_price=50.00
        ))

        self.product_with_an_empty_value = json.dumps(dict(
            product_id=1,
            category='',
            product_name='coffee',
            quantity=100,
            unit_price=50.00
        ))

        self.product_with_non_string_product_name = json.dumps(dict(
            product_id=1,
            category='beverages',
            product_name=8,
            quantity=100,
            unit_price=50.00
        ))

        self.product_with_non_string_category = json.dumps(dict(
            product_id=1,
            category=8,
            product_name='coffee',
            quantity=100,
            unit_price=50.00
        ))

        self.product_with_non_integer_quantity = json.dumps(dict(
            product_id=1,
            category='beverages',
            product_name='coffee',
            quantity='hundred',
            unit_price=50.00
        ))

        self.product_with_non_positive_integer_quantity = json.dumps(dict(
            product_id=1,
            category='beverages',
            product_name='coffee',
            quantity=-100,
            unit_price=50.00
        ))

        self.product_with_non_float_price = json.dumps(dict(
            product_id=1,
            category='beverages',
            product_name='coffee',
            quantity=100,
            unit_price=50
        ))

        self.product_with_non_positive_float_price = json.dumps(dict(
            product_id=1,
            category='beverages',
            product_name='coffee',
            quantity=100,
            unit_price=-50.00
        ))

        self.update_product = json.dumps(dict(
            category='beverages',
            product_name='tea',
            quantity=100,
            unit_price=50.00
        ))

        self.sale = json.dumps(dict(
            product_id=2,
            quantity=10
        ))

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
   
    def test_admin_user_create(self):
        """ Test API can create user """
        resp = self.client.post(
            '/api/v1/register', data=self.test_admin_user, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = json.loads(resp.data.decode())

    def test_create_an_existing_user(self):
        """ Test API cannnot recreate an already exisiting user """
        resp = self.client.post(
            '/api/v1/register', data=self.test_admin_user, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == 'That email is already registered, please login!')

    def test_create_user_with_blank_value(self):
        """ Test API cannnot create a user using blank values """
        resp = self.client.post(
            '/api/v1/register', data=self.test_blank_value_user, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "Sorry, there's an empty user value, please check your input values")

    def test_create_user_with_invalid_email(self):
        """ Test API cannnot create a user using an invalid email address """
        resp = self.client.post(
            '/api/v1/register', data=self.test_invalid_email_user, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "Please use a valid email address")

    def test_create_user_with_non_boolean_is_admin_value(self):
        """ Test API cannnot create a user using a non boolean is_admin value """
        resp = self.client.post(
            '/api/v1/register', data=self.test_non_boolean_is_admin_value_user, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "is_admin value must be a boolean!")

    def test_create_user_with_a_short_password(self):
        """ Test API cannnot create a user using a short password """
        resp = self.client.post(
            '/api/v1/register', data=self.test_short_password, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "password is too short, it should be more than 6 characters!")

    def test_admin_user_login(self):
        """ Test API can create user """
        resp = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_a_get_token(self):
        """ Test token generation during login """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        self.assertEqual(test_admin_user_login.status_code, 200)

    def test_create_product(self):
        """ Test API can create a product """
        self.client.post(
            '/api/v1/register', data=self.test_admin_user, content_type='application/json')
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 201)

    def test_create_product_with_an_empty_value(self):
        """ Test API cannot create a product with an empty value """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product_with_an_empty_value,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "Sorry, there's an empty value, please check your input values")

    def test_create_product_with_non_string_product_name(self):
        """ Test API cannot create a product with a non-string product_name """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product_with_non_string_product_name,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "A product name's value must be a string")

    def test_create_product_with_non_string_category(self):
        """ Test API cannot create a product with a non-string product_name """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product_with_non_string_category,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "A category's value must be a string")

    def test_create_product_with_non_integer_quantity(self):
        """ Test API cannot create a product with a non-integer quantity """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product_with_non_integer_quantity,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "A quantity's value must be an integer")

    def test_create_product_with_non_positive_integer_quantity(self):
        """ Test API cannot create a product with a non-positive integer quantity """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product_with_non_positive_integer_quantity,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "A quantity's value must be a positive integer")

    def test_create_product_with_non_float_price(self):
        """ Test API cannot create a product with a non-string product_name """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product_with_non_float_price,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "A price's value must be of float data type")

    def test_create_product_with_non_positive_float_price(self):
        """ Test API cannot create a product with a non-positive float price """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product_with_non_positive_float_price,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "A price's value must be a positive float")

    def test_create_xisting_product(self):
        """ Test API can create a product """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/products',
                                data=self.product,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "Sorry, such a product already exists, please confirm its category")

    def test_get_all_products(self):
        """ Test API can retrieve all products """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        response = self.client.get(
            '/api/v1/products', content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(response.status_code, 200)

    def test_get_specific_product(self):
        """ Test API can retrieve all products """

        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        response = self.client.get(
            '/api/v1/products/1', content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        """ Test API can retrieve all products """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]

        resp = self.client.put('/api/v1/products/1',
                               data=self.update_product,
                               content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 200)

        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "update successful!")

    def test_make_sale(self):
        """ Test API cannot allow an admin user make a sale """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]

        resp = self.client.post('/api/v1/sales',
                                data=self.sale,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))

        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'],
                         "Attendant rights required!")

    def test_get_all_sales(self):
        """ Test API allows an admin user get all sales """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]

        resp = self.client.get('/api/v1/sales',
                               data=self.sale,
                               content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 200)

    def test_get_a_specific_sale(self):
        """ Test API cannot allow an admin get a specific sale """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]

        resp = self.client.get('/api/v1/sales/1',
                               data=self.sale,
                               content_type='application/json', headers=dict(Authorization="Bearer " + token))
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'],
                         "Attendant rights required!")

    def test_xdelete_product(self):
        """ Test API can delete a specific products """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.delete('/api/v1/products/1',
                                  content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 200)

        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'],
                         "delete operation successful!")
    
    def test_xlogout_admin(self):
        """ Test API cannot allow an admin user make a sale """
        test_admin_user_login = self.client.post(
            '/api/v1/login', data=self.user_login, content_type='application/json')
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]

        resp = self.client.post('/api/v1/logout',
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))

        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'],
                         "Successfully logged out")
        users.clear()
    
    def test_xttendant_create_user(self):
        """ Test API can create an attendant user """
        resp = self.client.post(
            '/api/v1/register', data=self.test_attendant_user, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_xttendant_user_login(self):
        """ Test API can allow attendant user login """
        resp = self.client.post(
            '/api/v1/login', data=self.attendant_user_login, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
    
    def test_xttendant_make_sale(self):
        """ Test API can allow an attendant make a sale """
        test_attendant_user_login = self.client.post(
            '/api/v1/login', data=self.attendant_user_login, content_type='application/json')
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = self.client.post('/api/v1/sales',
                                data=self.sale,
                                content_type='application/json', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(resp.status_code, 201)

    def teardown(self):
        self.app_context.pop()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
