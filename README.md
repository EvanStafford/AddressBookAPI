# AddressBookAPI

AddressBookAPI.py contains the API itself.

APIDatabase.py contains a class that the API uses to interact with Elasticsearch.

test_AddressBookAPI.py contains the unit tests.

elastic_host_config.json is a short json file containing the host and port information that gets passed to Elasticsort() in APIDatabase.py. It should be changed to match the Elasticsearch server. I haven't tested it with different setups, but hopefully it works.

The steps I took on my machine to get the API running (after installing the necessary software):

-start the Elasticsearch server (involves running bin/elasticsearch or bin\elasticsearch.bat)

-set the environment variable FLASK_APP=AddressBookAPI.py

-execute "flask run"

-access the API endpoints through http://127.0.0.1:5000

The API stores contacts in an Elasticsearch index named "address-book" by default, though this can be changed by passing a different index name to APIDatabase(). A contact consists of a name, email address, phone number, and postal address all stored as strings. The name is the only field that must be nonempty. I decided to write things such that the API doesn't accept any fields other than these and returns an error if extra fields are present. Contacts are stored in the server with the names serving as their ids, since it was required that the names be unique. Because of this, I decided it was necessary to make it so that names cannot be updated with PUT. Less than ideal, but by the time I noticed it I didn't have time to redesign it.

The unit testing is not nearly as fleshed out as I would have liked, and one of the tests fails for reasons I didn't manage to figure out. If I were to do this project over, I would make much better use of it when writing the database methods.
