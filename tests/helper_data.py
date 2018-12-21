import json


test_admin_user = json.dumps(dict(
    email='admin@test.com',
    is_admin=True,
    password="test123"
))

test_attendant_user = json.dumps(dict(
    email='attendant@test.com',
    is_admin=False,
    password="test123"
))

test_blank_value_user = json.dumps(dict(
    email='',
    is_admin=True,
    password="test123"
))

test_invalid_email_user = json.dumps(dict(
    email='test',
    is_admin=True,
    password="test123"
))

test_non_boolean_is_admin_value_user = json.dumps(dict(
    email='tests@test.com',
    is_admin="true",
    password="test123"
))

test_short_password = json.dumps(dict(
    email='testy@test.com',
    is_admin=True,
    password="test"
))

admin_user_login = json.dumps(dict(
    email='admin@test.com',
    password="test123"
))

attendant_user_login = json.dumps(dict(
    email='attendant@test.com',
    password="test123"
))

product = json.dumps(dict(
    product_id=1,
    category='beverages',
    product_name='coffee',
    quantity=100,
    unit_price=50.00
))

product_with_an_empty_value = json.dumps(dict(
    product_id=1,
    category='',
    product_name='coffee',
    quantity=100,
    unit_price=50.00
))

product_with_non_string_product_name = json.dumps(dict(
    product_id=1,
    category='beverages',
    product_name=8,
    quantity=100,
    unit_price=50.00
))

product_with_non_string_category = json.dumps(dict(
    product_id=1,
    category=8,
    product_name='coffee',
    quantity=100,
    unit_price=50.00
))

product_with_non_integer_quantity = json.dumps(dict(
    product_id=1,
    category='beverages',
    product_name='coffee',
    quantity='hundred',
    unit_price=50.00
))

product_with_non_positive_integer_quantity = json.dumps(dict(
    product_id=1,
    category='beverages',
    product_name='coffee',
    quantity=-100,
    unit_price=50.00
))

product_with_non_float_price = json.dumps(dict(
    product_id=1,
    category='beverages',
    product_name='coffee',
    quantity=100,
    unit_price=50
))

product_with_non_positive_float_price = json.dumps(dict(
    product_id=1,
    category='beverages',
    product_name='coffee',
    quantity=100,
    unit_price=-50.00
))

update_product = json.dumps(dict(
    category='beverages',
    product_name='tea',
    quantity=100,
    unit_price=50.00
))

sale = json.dumps(dict(
    product_id=1,
    quantity=10
))
# key errorx
user_without_password_key = json.dumps(dict(
    email='admin@test.com',
    is_admin=True
))

user_without_is_admin_key = json.dumps(dict(
    email='admin@test.com',
    password="test123"
))

user_without_email_key = json.dumps(dict(
    is_admin=True,
    password="test123"
))

product_without_price_key = json.dumps(dict(
    product_id=1,
    category='beverages',
    product_name='coffee',
    quantity=100
))

product_without_quantity_key = json.dumps(dict(
    product_id=1,
    category='beverages',
    product_name='coffee',
    unit_price=50.00
))

product_without_category_key = json.dumps(dict(
    product_id=1,
    product_name='coffee',
    quantity=100,
    unit_price=50.00
))

product_without_product_name_key = json.dumps(dict(
    product_id=1,
    category='beverages',
    quantity=100,
    unit_price=50.00
))