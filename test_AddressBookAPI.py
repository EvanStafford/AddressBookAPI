"""
python -m unittest test_AddressBookAPI.py
"""

import unittest
from elasticsearch import Elasticsearch
from APIDatabase import APIDatabase
import random
import string
import json

es = Elasticsearch()
es.indices.delete(index='test-index', ignore=[400,404])
db = APIDatabase(elastic_index='test-index')

data_model = {
    'name': '',
    'email': '',
    'phone': '',
    'postal_address': ''
}

random_contacts = []
characters = string.ascii_letters + string.digits + string.punctuation
for i in range(100):
    contact = data_model.copy()
    for k in data_model:
        contact[k] = ''.join(random.choice(characters) for c in range(random.randrange(1,50)))
    random_contacts.append(contact)

test_contact = {
    'name': 'Firstname Lastname',
    'email': 'test@example.com',
    'phone': '123-234-3456',
    'postal_address': '1234 Test Dr.'
}

test_contact_updated = {
    'name': 'Firstname Lastname',
    'email': 'test2@example.com',
    'phone': '123-333-3456',
    'postal_address': '5321 Test Dr.'
}

class testAPIDatabase(unittest.TestCase):
    def test_create(self):
        self.assertEqual(db.create_contact(test_contact), {'message': 'created', 'status':200})
        self.assertEqual(db.create_contact(test_contact), {'error': 'contact already exists', 'status': 409})
    
    def test_get_contact_by_name(self):
        db.create_contact(test_contact)
        self.assertEqual(db.get_contact_by_name(test_contact['name']), test_contact)
        self.assertEqual(db.get_contact_by_name('invalid name'), {'error': 'not found', 'status': 404})

    def test_update_contact(self):
        self.assertEqual(db.update_contact(test_contact['name'], test_contact), {'message':'noop', 'status': 200})
        self.assertEqual(db.update_contact(test_contact['name'], test_contact_updated), {'message':'updated', 'status': 200})
        self.assertEqual(db.get_contact_by_name(test_contact['name']), test_contact_updated)
        self.assertEqual(db.update_contact('invalid name', {'phone': '1234'}), {'error': 'not found', 'status': 404})
    
    def test_delete_contact(self):
        self.assertEqual(db.delete_contact(test_contact['name']), {'message': 'deleted', 'status': 200})
        self.assertEqual(db.delete_contact(test_contact['name']), {'error': 'not found', 'status': 404})

    def test_get_contact_by_query(self):
        db.create_contact(test_contact_updated)
        self.assertEqual(db.get_contact_by_query(10, 0, '*'), [test_contact_updated])
        
if __name__ == '__main__':
    unittest.main()