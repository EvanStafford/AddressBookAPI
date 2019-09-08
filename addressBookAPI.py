"""
To run on Mac/Linux:
$ export FLASK_APP=AddressBookAPI.py
$ flask run

To run on Windows Command Prompt:
>set FLASK_APP=AddressBookAPI.py
>flask run

To run on Windows PowerShell:
> $env:Flask_APP = "AddressBookAPI.py"
> flask run

Then navigate to http://127.0.0.1:5000/
"""

from flask import Flask, request, escape, jsonify
from APIDatabase import APIDatabase

app = Flask(__name__)

# this dict defines the data model for a contact
contact_data_model = {
    'name': '',
    'email': '',
    'phone': '',
    'postal_address': ''
}
# this dict contains conditions that the contact data is required to satisfy
contact_data_conditions = {
    'name': lambda s : len(s) < 1000,
    'email': lambda s : s=='' or ('@' in s and len(s) < 1000),
    'phone': lambda s : len(s) < 50,
    'postal_address': lambda s : len(s) < 1000
}

# connect to the database and gain access to methods for interacting with it
db = APIDatabase()

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        page_size = request.args.get('pageSize', 10, type=int)
        page = request.args.get('page', 0, type=int)
        query_string = request.args.get('query', '*')

        result = db.get_contact_by_query(page_size, page * page_size, query_string)
        return (jsonify(result), result['status'] if 'error' in result else 200)

    elif request.method == 'POST':
        new_contact = contact_data_model.copy()
        
        # ensure there were not fields outside the data model that were passed, and 
        # ensure the data values provided conform to the given conditions
        for field in request.args: 
            value = request.args.get(field)
            if field not in contact_data_model:
                return {'error': 'invalid contact field [{}]'.format(field), 'status': 400}, 400
            elif not contact_data_conditions[field](value):
                return {'error': 'invalid contact value for [{}]'.format(field), 'status': 400}, 400
            else:
                new_contact[field] = value

        result = db.create_contact(new_contact)
        return result, result['status']

@app.route('/contact/<name>', methods=['GET', 'PUT', 'DELETE'])
def named_contact(name):
    if request.method == 'GET':
        result = db.get_contact_by_name(escape(name))
        return result, 404 if 'error' in result else 200

    elif request.method == 'PUT':
        contact_details = {}
        
        # ensure there were not fields outside the data model that were passed, and 
        # ensure the data values provided conform to the given conditions
        for field in request.args:
            value = request.args.get(field)
            if field not in contact_data_model:
                return {'error': 'invalid contact field [{}]'.format(field), 'status': 400}, 400
            elif not contact_data_conditions[field](value):
                return {'error': 'invalid contact value for [{}]'.format(field), 'status': 400}, 400
            else:
                contact_details[field] = value

        # prevent the contact name from changing (this is needed because the contact
        # name is used as the Elasticsearch id)
        if 'name' in contact_details and name != contact_details['name']:
            return {'error': 'parameter [name] mismatch', 'status': 400}, 400
        
        result = db.update_contact(escape(name), contact_details)
        return result, result['status']
        
    elif request.method == 'DELETE':
        result = db.delete_contact(escape(name))
        return result, result['status']
















