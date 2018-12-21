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

    def test_get_specific_sale_item(self):
        # """ Test API cannot allow an admin get a specific sale """
        users.clear()
        user_registration(self, test_admin_user)
        test_admin_user_login = user_login(self, admin_user_login)
        response_content = json.loads(test_admin_user_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = get_specific_sale(self, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Attendant rights required!")
    
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

    def teardown(self):
        super(SaleTestCase, self).teardown()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()