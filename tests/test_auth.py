from .base import *


class UserTestCase(BaseTestCase):
    """ This class represents the product test case """
    
    
    def setUp(self):
        super(UserTestCase, self).setUp()
   
    def test_create_admin(self):
        users.clear()
        # """ Test API can create user """
        resp = user_registration(self, test_admin_user)
        self.assertEqual(resp.status_code, 201)
        response = json.loads(resp.data.decode())

    def test_admin_login(self):
        # """ Test API can create user """
        resp = user_login(self, admin_user_login)
        self.assertEqual(resp.status_code, 200)
    
    def test_admin_logout(self):
        # """ Test API cannot allow an admin user make a sale """
        users.clear()
        resp = user_registration(self, test_admin_user)
        admin_login = user_login(self, admin_user_login)
        response_content = json.loads(admin_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = user_logout(self, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Successfully logged out")

    def test_create_attendant(self):
        # """ Test API can create an attendant user """
        users.clear()
        resp = user_registration(self, test_attendant_user)
        self.assertEqual(resp.status_code, 201)

    def test_attendant_login(self):
        # """ Test API can allow attendant user login """
        users.clear()
        resp = user_registration(self, test_attendant_user)
        resp = user_login(self, attendant_user_login)
        self.assertEqual(resp.status_code, 200)

    def test_attendant_logout(self):
        # """ Test API cannot allow an admin user make a sale """
        users.clear()
        resp = user_registration(self, test_attendant_user)
        attendant_login = user_login(self, attendant_user_login)
        response_content = json.loads(attendant_login.data.decode('utf-8'))
        token = response_content["access_token"]
        resp = user_logout(self, token)
        response_data = json.loads(resp.data.decode())
        self.assertEqual(response_data['message'], "Successfully logged out")

    def test_create_an_existing_user(self):
        # """ Test API cannnot recreate an already exisiting user """
        resp = user_registration(self, test_admin_user)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == 'That email is already registered, please login!')

    def test_missing_password_key(self):
        resp = user_registration(self, user_without_password_key)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "'password' key missing")

    def test_missing_is_admin_key(self):
        resp = user_registration(self, user_without_is_admin_key)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "'is_admin' key missing")

    def test_missing_email_key(self):
        resp = user_registration(self, user_without_email_key)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "'email' key missing")


    def test_create_user_with_blank_value(self):
        # """ Test API cannnot create a user using blank values """
        resp = user_registration(self, test_blank_value_user)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "Sorry, there's an empty user value, please check your input values")

    def test_create_user_with_invalid_email(self):
        # """ Test API cannnot create a user using an invalid email address """
        resp = user_registration(self, test_invalid_email_user)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "Please use a valid email address")

    def test_create_user_with_non_boolean_is_admin_value(self):
        # """ Test API cannnot create a user using a non boolean is_admin value """
        resp = user_registration(self, test_non_boolean_is_admin_value_user)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "is_admin value must be a boolean!")

    def test_create_user_with_a_short_password(self):
        # """ Test API cannnot create a user using a short password """
        resp = user_registration(self, test_short_password)
        self.assertEqual(resp.status_code, 400)
        response = json.loads(resp.data.decode())
        self.assertTrue(
            response['message'] == "password is too short, it should be more than 6 characters!")

    def teardown(self):
        super(UserTestCase, self).teardown()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
