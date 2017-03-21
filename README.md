# Startup
* virtualenv, etc. installed packages include
  *   Flask
  *   Flask-HTTPAuth
  *   (nose and pytest for tests)
* python app.py

# Endpoints
Everything lives off /contacts/api/1.0/contacts
* GET index
* GET <contact_id>
* POST a new contact
* PUT an update to an existing contact
* DELETE a contact by id
* POST to /search with parameters

# Areas for improvement
* Right now the only fields available for a contact are name, phone, address, and email. It might be nice to allow the user to make a new contact with any field they like (minus a few protected fields, such as id and timestamps), and to allow update in a similar manner.
* It'd be nice to have a create new user endpoint.

# Acknowledgements
Miguel Grinberg wrote a [blog post](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) along these very lines. I referenced that post in writing this API. I've found his other posts to be similarly well constructed.
