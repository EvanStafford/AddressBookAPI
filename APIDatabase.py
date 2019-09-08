class APIDatabase:
    def __init__(self, elastic_index='address-book', *args, **kwargs):
        # calls Elasticsearch() to connect to the database and creates the index for the address book if needed
        import json
        from elasticsearch import Elasticsearch
        from elasticsearch import exceptions as es_exceptions
        # hold on to the exceptions so they can be recognized in the try...except blocks later
        self.es_exceptions = es_exceptions

        # host and port information for Elasticshare() is in a separate json file
        try:
            with open('./elastic_host_config.json') as f:
                elastic_host_info = json.load(f)
        except FileNotFoundError:
            elastic_host_info = {'host': 'localhost', 'port': 9200}
        
        self.database = Elasticsearch(elastic_host_info, *args, **kwargs)
        self.elastic_index = elastic_index
        
        # ensure the Elasticsearch index exists
        self.database.indices.create(index=elastic_index, ignore=400)

    def get_contact_by_query(self, page_size, page_num, query_string):
        # searches the data store using query_string and returns page_size entries starting on page page_num
        
        if page_size < 0:
            return {'error': 'pageSize must be a nonnegative integer', 'status':400}
        elif page_num < 0:
            return {'error': 'page must be a nonnegative integer', 'status':400}

        try:
            result = self.database.search(index=self.elastic_index, from_=page_num, q=query_string, size=page_size)
            return [contact['_source']['doc'] for contact in result['hits']['hits']]
        except self.es_exceptions.RequestError as err:
            return {'error': err.info['error']['root_cause'][0]['reason'], 'status': err.status_code}
    
    def get_contact_by_name(self, name):
        # returns the contact with the given name
        try:
            return self.database.get_source(index=self.elastic_index, id=name)['doc']
        except self.es_exceptions.NotFoundError:
            return {'error': 'not found', 'status': 404}

    def create_contact(self, contact_details):
        # creates a contact with the given contact_details (which includes a name)
        try:
            self.database.create(index=self.elastic_index, id=contact_details['name'], body={'doc': contact_details})
            return {'message': 'created', 'status': 200}
        except self.es_exceptions.ConflictError:
            return {'error': 'contact already exists', 'status': 409}
    
    def update_contact(self, name, contact_details):
        # updates a contact with the new contact_details
        try:
            result = self.database.update(index=self.elastic_index, id=name, body={'doc': {'doc': contact_details}})
            return {'message': result['result'], 'status': 200}
        except self.es_exceptions.NotFoundError:
            return {'error': 'not found', 'status': 404}
    
    def delete_contact(self, name):
        # deletes the contact with the given name
        try:
            self.database.delete(index=self.elastic_index, id=name)
            return {'message': 'deleted', 'status': 200}
        except self.es_exceptions.NotFoundError:
            return {'error': 'not found', 'status': 404}

    
            
    


