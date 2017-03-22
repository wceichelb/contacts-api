# Startup
* Set up a virtual environment. Installed packages include
    * Flask
    * Flask-HTTPAuth
    * (nose and pytest for tests)
* `python app.py`

# Endpoints

Everything lives off of /contacts/api/1.0/contacts

### GET an index of contacts

* URL: it's just the root url
* Method: GET
* URL Params: none
* Data Params: none
* Successful Response
    * Code: 200
    * Content: `{'contacts': [a list of contacts]}`
* Error Response
    * None. If you hit it it'll give you back the index
* Example call
        * `curl -i localhost:5000/contacts/api/1.0/contacts`

### GET `<contact_id>`
* URL: `root/<int:contact_id>`
* Method: GET
* URL Params: `contact_id=[integer]`
* Data Params: none
* Successful Response
    * Code: 200
    * Content: `{'contact': {a contact}}`
* Error Response
     * Code: 404
     * Content: `{'error': 'Not Found'}`
* Example call
    * `curl -i localhost:5000/contacts/api/1.0/contacts/1`

### POST a new contact
* URL: Just the root again
* Method: POST
* URL Params: none
* Data Params: a JSON blob containing at least a value for `'name'`
* Successful Response
    * Code: 201
    * Content: `{'contact': {the new contact}}`
* Error Response
    * Code: 400
    * Content: `{'error': 'Bad Request'}`
    * Code: 401
    * Content: `{'error': 'Unauthorized'}`
* Example call
    * `curl -u user:password -i -H "Content-Type: application/json" -X POST -d '{"name":"a name"}' localhost:5000/contacts/api/1.0/contacts`
* Note: requires an authenticated user

### PUT an update to an existing contact
* URL: `root/<int:contact_id>`
* Method: PUT
* URL Params: contact_id=[integer]
* Data Params: a JSON blob in which keys are fields to update and values are values to update to
* Successful Response
    * Code: 201
    * Content: `{'contact': {the updated contact}}`
* Error Response
    * Code: 400
    * Content: `{'error': 'Bad Request'}`
    * Code: 401
    * Content: `{'error': 'Unauthorized'}`
    * Code: 404
    * Content: `{'error': 'Not Found'}` (returned if contact with `contact_id` doesn't exist)
    * Code: 405
    * Content: `{'error': 'Not Allowed'}` (returned if user tries to updated protected field)
* Example call
    * `curl -u user:password -i -H "Content-Type: application/json" -X POST -d '{"name":"a name"}' localhost:5000/contacts/api/1.0/contacts/1`
* Note: requires an authenticated user

### DELETE a contact by id
* URL: `root/<int:contact_id>`
* Method: DELETE
* URL Params: contact_id=[integer]
* Data Params: none
* Successful Response
    * Code: 201
    * Content: `{'contact': {the deleted contact}}`
* Error Response
    * Code: 401
    * Content: `{'error': 'Unauthorized'}`
    * Code: 404
    * Content: `{'error': 'Not Found'}` (returned if contact with `contact_id` doesn't exist)
* Example call
    * `curl -u user:password -i -H "Content-Type: application/json" -X DELETE '{"name":"a name"}' localhost:5000/contacts/api/1.0/contacts/1`
* Note: requires an authenticated user

### POST to /search with parameters
* URL: `root/search`
* Method: POST
* URL Params: none
* Data Params: a JSON blob of the form `{'terms': {'field to search on': 'value to search by'}}`
* Successful Response
    * Code: 201
    * Content: `{'contacts': [a list of contacts]}`
    * Note: if no contacts match the terms, an empty list is returned. (Could add a flag to get 404 in this case?)
* Error Response
    * Code: 400
    * Content: `{'error': 'Bad Request'}` (if not JSON or no `'terms'`)
* Example call
    * `curl -i -H "Content-Type: application/json" -X POST '{'terms': {"name":"a name"}}' localhost:5000/contacts/api/1.0/contacts/search`

# Areas for improvement
* Right now the only fields available for a contact are name, phone, address, and email. It might be nice to allow the user to make a new contact with any field they like (minus a few protected fields, such as id and timestamps), and to allow update in a similar manner.
* It'd be nice to have a create new user endpoint.

# Acknowledgements
Miguel Grinberg wrote a [blog post](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) along these very lines. I referenced that post in writing this API. I've found his other posts to be similarly well constructed.
