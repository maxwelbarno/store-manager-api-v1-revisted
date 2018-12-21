from .base import *

class ProductTestCase(BaseTestCase):
    """ This class represents the product test case """
    
    def setUp(self):
        super(ProductTestCase, self).setUp()

    def test_create_product(self):
        # """ Test API can create a product """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product, token)
        self.assertEqual(resp.status_code, 201)

    def test_create_product_with_missing_product_name_key(self):
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_without_product_name_key, token)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "'product_name' key missing")

    def test_create_product_with_missing_product_category_key(self):
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_without_category_key, token)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "'category' key missing")

    def test_create_product_with_missing_quantity_key(self):
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_without_quantity_key, token)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "'quantity' key missing")

    def test_create_product_with_missing_price_key(self):
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_without_price_key, token)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "'unit_price' key missing")

    # def test_create_product_with_an_empty_value(self):
    #     # """ Test API cannot create a product with an empty value """
    #     users.clear()
    #     user_registration(self, test_admin_user)
    #     admin_login = user_login(self, admin_user_login)
    #     response_content = json.loads(admin_login.data.decode('utf-8'))
    #     token = response_content["access_token"]
    #     resp = resp = create_product(self, product_with_an_empty_value, token)
    #     self.assertEqual(resp.status_code, 400)
    #     response = json.loads(resp.data.decode())
    #     self.assertTrue(response['message'] == "Sorry, there's an empty value, please check your input values")

    # def test_create_product_with_blank_product_name_value(self):
    #     # """ Test API cannot create a product with an empty value """
    #     users.clear()
    #     user_registration(self, test_admin_user)
    #     admin_login = user_login(self, admin_user_login)
    #     response_content = json.loads(admin_login.data.decode('utf-8'))
    #     token = response_content["access_token"]
    #     resp = resp = create_product(self, product_with_blank_product_name_value, token)
    #     self.assertEqual(resp.status_code, 400)
    #     response = json.loads(resp.data.decode())
    #     self.assertTrue(response['message'] == "Sorry, there's an empty value, please check your input values")

    def test_create_product_with_non_string_product_name(self):
        # """ Test API cannot create a product with a non-string product_name """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_with_non_string_product_name, token)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "A product name's value must be a string")

    def test_create_product_with_non_string_category(self):
        # """ Test API cannot create a product with a non-string product_name """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_with_non_string_category, token)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "A category's value must be a string")

    def test_create_product_with_non_integer_quantity(self):
        # """ Test API cannot create a product with a non-integer quantity """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_with_non_integer_quantity, token)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "A quantity's value must be an integer")

    def test_create_product_with_non_positive_integer_quantity(self):
        # """ Test API cannot create a product with a non-positive integer quantity """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_with_non_positive_integer_quantity, token)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "A quantity's value must be a positive integer")

    def test_create_product_with_non_float_price(self):
        # """ Test API cannot create a product with a non-float price """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_with_non_float_price, token)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "A price's value must be of float data type")

    def test_create_product_with_non_positive_float_price(self):
        # """ Test API cannot create a product with a non-positive float price """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product_with_non_positive_float_price, token)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "A price's value must be a positive float")

    def test_create_an_existing_product(self):
        # """ Test API cannot create an existing product """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        #create same product twice
        create_product(self, product, token)
        resp = create_product(self, product, token)
        products.clear()
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "Sorry, such a product already exists, please confirm its category")

    def test_get_all_products(self):
        # """ Test API can retrieve all products """
        products.clear()
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        response = get_all_products(self, token)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data.decode())
        self.assertTrue(response['message'] == "Success")
    
    def test_get_non_existing_products(self):
        # """ Test API can retrieve all products """
        products.clear()
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        response = get_all_products(self, token)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data.decode())
        self.assertTrue(response['message'] == "No product record(s) available")

    def test_get_specific_product(self):
        # """ Test API can retrieve all products """
        users.clear()
        products.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = create_product(self, product, token)
        response = get_specific_product(self, token)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_specific_product(self):
        # """ Test API can retrieve all products """
        users.clear()
        products.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        response = get_specific_product(self, token)
        self.assertEqual(response.status_code, 404)
        response = json.loads(response.data.decode())
        self.assertTrue(response['message'] == "Sorry, the product does not exist!")

    def test_update_product(self):
        # """ Test API can retrieve all products """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = product_update(self, update_product, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "update successful!")

    def test_update_product_with_missing_product_name_key(self):
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = product_update(self, update_product_without_product_name_key, token)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "'product_name' key missing")

    def test_update_product_with_missing_category_key(self):
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = product_update(self, update_product_without_category_key, token)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "'category' key missing")

    def test_update_product_with_missing_quantity_key(self):
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = product_update(self, update_product_without_quantity_key, token)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "'quantity' key missing")

    def test_update_product_with_missing_price_key(self):
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = product_update(self, update_product_without_price_key, token)
        response = json.loads(resp.data.decode())
        self.assertTrue(response['message'] == "'unit_price' key missing")

    def test_delete_product(self):
        # """ Test API can delete a specific products """
        users.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = delete_specific_product(self, token)
        self.assertEqual(resp.status_code, 200)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "delete operation successful!")

    def test_delete_non_existing_product(self):
        # """ Test API can delete a specific products """
        users.clear()
        products.clear()
        user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = delete_specific_product(self, token)
        self.assertEqual(resp.status_code, 404)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Sorry, the product does not exist!")

    def teardown(self):
        super(ProductTestCase, self).teardown()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
