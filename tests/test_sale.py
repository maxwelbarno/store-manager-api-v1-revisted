from .base import *

class SaleTestCase(BaseTestCase):
    """ This class represents sales test case """
    
    def setUp(self):
        super(SaleTestCase, self).setUp()

    def test_make_sale(self):
        # """ Test API cannot allow an admin user make a sale """
        users.clear()
        user_registration(self, test_admin_user)
        test_admin_user_login = user_login(self, admin_user_login)
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = make_sale(self, sale, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Attendant rights required!")

    def test_get_all_sales(self):
        # """ Test API allows an admin user get all sales """
        users.clear()
        user_registration(self, test_admin_user)
        test_admin_user_login = user_login(self, admin_user_login)
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        make_sale(self, sale, token)
        resp = get_all_sales(self, token)
        self.assertEqual(resp.status_code, 200)

    def test_get_non_existent_sales(self):
        # """ Test API allows an admin user get all sales """
        users.clear()
        sales.clear()
        user_registration(self, test_admin_user)
        test_admin_user_login = user_login(self, admin_user_login)
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        # make_sale(self, sale, token)
        resp = get_all_sales(self, token)
        # self.assertEqual(resp.status_code, 200)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "No sale record(s) available")

    def test_admin_get_specific_sale_item(self):
        # """ Test API cannot allow an admin get a specific sale """
        users.clear()
        user_registration(self, test_admin_user)
        test_admin_user_login = user_login(self, admin_user_login)
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = get_specific_sale(self, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Attendant rights required!")

    def test_attendant_get_specific_sale_item(self):
        # """ Test API cannot allow an admin get a specific sale """
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = get_specific_sale(self, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Success")
    
    def test_get_non_existent_specific_sale_item(self):
        # """ Test API cannot allow an admin get a specific sale """
        users.clear()
        sales.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = get_specific_sale(self, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Sorry, sale record does not exist")
    
    def test_attendant_make_sale(self):
        # """ Test API can allow an attendant make a sale """
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = make_sale(self, sale, token)
        self.assertEqual(resp.status_code, 201)

    def test_sale_non_existent_product(self):
        # """ Test API can allow an attendant make a sale """
        users.clear()
        products.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = make_sale(self, sale, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Warning! You are attempting to sale a non-existent product")

    def test_sale_insufficient_quantity(self):
        # """ Test API can allow an attendant make a sale """
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = make_sale(self, insufficient_product_sale, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Insufficient stock")

    def test_make_sale_with_blank_value(self):
        # """ Test API can allow an attendant make a sale """
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = make_sale(self, sale_with_blank_value, token) 
        self.assertEqual(resp.status_code, 400)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Sorry, there's an empty value, please check your input values")

    def test_make_sale_with_non_int_product_id_value(self):
        # """ Test API can allow an attendant make a sale """
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = make_sale(self, sale_with_non_int_product_id_value, token) 
        self.assertEqual(resp.status_code, 400)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "A sale id's value must be an int")

    def test_make_sale_with_non_int_quantity_value(self):
        # """ Test API can allow an attendant make a sale """
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = make_sale(self, sale_with_non_int_quantity_value, token) 
        self.assertEqual(resp.status_code, 400)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "A quantity's value must be an integer")

    def test_make_sale_with_non_positive_quantity_value(self):
        # """ Test API can allow an attendant make a sale """
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = make_sale(self, sale_with_non_positive_quantity_value, token) 
        self.assertEqual(resp.status_code, 400)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "quantity cannot be less than one")

    def test_sale_product_without_quantity_key(self):
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = make_sale(self, sale_product_without_quantity_key, token)
        response_data = json.loads(resp.data.decode())
        self.assertTrue(response_data['message'] == "'quantity' key missing")

    def test_sale_product_without_product_id_key(self):
        users.clear()
        user_registration(self, test_attendant_user)
        test_attendant_user_login = user_login(self, attendant_user_login)
        response_content = json.loads(test_attendant_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        create_product(self, product, token)
        resp = make_sale(self, sale_product_without_product_id_key, token)
        response_data = json.loads(resp.data.decode())
        self.assertTrue(response_data['message'] == "'product_id' key missing")

    def teardown(self):
        super(SaleTestCase, self).teardown()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()