"""
run with:
python -m unittest test_AddressBookAPI.py
"""

import unittest
from elasticsearch import Elasticsearch
from APIDatabase import APIDatabase

es = Elasticsearch()
db = APIDatabase(elastic_index='test-index')

test_contact = {
            'name': 'Firstname Lastname',
            'email': 'test@example.com',
            'phone': '123-234-3456',
            'postal_address': '1234 Test Dr.'
        }

class testAPIDatabase(unittest.TestCase):
    def test_create_contact(self):
        # start each test with an empty index
        es.indices.delete('test-index', ignore=[400, 404])
        es.indices.create('test-index', ignore=[400, 404])

        self.assertEqual(db.create_contact(test_contact), {'message': 'created', 'status':200})
        self.assertEqual(db.create_contact(test_contact), {'error': 'contact already exists', 'status': 409})
        self.assertEqual(db.create_contact(test_contact), {'error': 'contact already exists', 'status': 409})
        # if name is '', the AddressBookAPI gives a 404
    
    def test_get_contact_by_name(self):
        es.indices.delete('test-index', ignore=[400, 404])
        es.indices.create('test-index', ignore=[400, 404])
        db.create_contact(test_contact)

        self.assertEqual(db.get_contact_by_name(test_contact['name']), test_contact)
        self.assertEqual(db.get_contact_by_name(test_contact['name']), test_contact)
        self.assertEqual(db.get_contact_by_name('invalid name'), {'error': 'not found', 'status': 404})

    def test_update_contact(self):
        es.indices.delete('test-index', ignore=[400, 404])
        es.indices.create('test-index', ignore=[400, 404])
        db.create_contact(test_contact)

        test_contact_updated = {
            'name': 'Firstname Lastname',
            'email': 'test2@example.com',
            'phone': '123-333-3456',
            'postal_address': '5321 Test Dr.'
        }
        
        self.assertEqual(db.update_contact(test_contact['name'], test_contact), {'message':'noop', 'status': 200})
        self.assertEqual(db.update_contact(test_contact['name'], test_contact_updated), {'message':'updated', 'status': 200})
        self.assertEqual(db.get_contact_by_name(test_contact['name']), test_contact_updated)
        self.assertEqual(db.update_contact('invalid name', {'phone': '1234'}), {'error': 'not found', 'status': 404})
    
    def test_delete_contact(self):
        es.indices.delete('test-index', ignore=[400, 404])
        es.indices.create('test-index', ignore=[400, 404])
        db.create_contact(test_contact)

        self.assertEqual(db.delete_contact(test_contact['name']), {'message': 'deleted', 'status': 200})
        self.assertEqual(db.delete_contact(test_contact['name']), {'error': 'not found', 'status': 404})

    def test_get_contact_by_query(self):
        es.indices.delete('test-index', ignore=[400, 404])
        es.indices.create('test-index', ignore=[400, 404])
        db.create_contact(test_contact)

        # this one fails; didn't manage to figure out why
        self.assertEqual(db.get_contact_by_query(10, 0, '*'), [test_contact])
        
if __name__ == '__main__':
    unittest.main()