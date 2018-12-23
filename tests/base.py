import json
import os
import unittest
import sys
sys.path.append('../')
from flask import current_app
from app import create_app
from app.api.models import products, users, sales
from unittest import TestCase
from .helper_data import *

def user_registration(self, data):
        return self.client.post(
            'api/v1/register',
            data=data,
            content_type='application/json')

def user_login(self, data):
    return self.client.post(
        'api/v1/login',
        data=data,
        content_type='application/json')

def user_logout(self, token):
    return self.client.post(
        'api/v1/logout',
        content_type='application/json', 
        headers=dict(Authorization="Bearer " + token))

def create_product(self, data, token):
    return self.client.post(
        
        '/api/v1/products',
        data=data,
        content_type='application/json', 
        headers=dict(Authorization="Bearer " + token))

def get_all_products(self, token):
    return self.client.get(
        '/api/v1/products',
        content_type='application/json', 
        headers=dict(Authorization="Bearer " + token))

def get_specific_product(self, token):
    return self.client.get(
        '/api/v1/products/1',
        content_type='application/json', 
        headers=dict(Authorization="Bearer " + token))

def product_update(self, data, token):
    return self.client.put(
        '/api/v1/products/1',
        data=data,
        content_type='application/json', 
        headers=dict(Authorization="Bearer " + token))

def make_sale(self, data, token):
    return self.client.post(
        '/api/v1/sales',
        data=data,
        content_type='application/json', 
        headers=dict(Authorization="Bearer " + token))

def get_all_sales(self, token):
    return self.client.get(
        '/api/v1/sales',
        content_type='application/json', 
        headers=dict(Authorization="Bearer " + token))

def get_specific_sale(self, token):
    return self.client.get(
        '/api/v1/sales/1',
        content_type='application/json', 
        headers=dict(Authorization="Bearer " + token))

def delete_specific_product(self, token):
    return self.client.delete(
        '/api/v1/products/1',
        content_type='application/json',
        headers=dict(Authorization="Bearer " + token))

        

class BaseTestCase(TestCase):
    """ Base Tests """

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    
    def teardown(self):
        self.app_context.pop()

        