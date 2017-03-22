import time
from flask import Flask, jsonify, request, abort, make_response, url_for
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
auth = HTTPBasicAuth()

# AUTH
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

users = {
        'bomtoonen': 'password'
        }

contacts = [
        {
            'id': 1,
            'name': 'Peter Sagan',
            'phone': '123456789',
            'address': 'somewhere in Slovakia?',
            'email': 'peto@sagan.com',
            'created_at': str(time.time())
            },
        {
            'id': 2,
            'name': 'Chris Froome',
            'phone': '2222222222',
            'address': 'London',
            'email': 'froome@sky.net',
            'created_at': str(time.time())
            }
        ]

# ROUTES
@app.route('/contacts/api/1.0/contacts', methods=['GET'])
def index_contacts():
    return jsonify({'contacts':[make_contact_with_uri(c) for c in contacts]})

@app.route('/contacts/api/1.0/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = [c for c in contacts if c['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    return jsonify({'contact':make_contact_with_uri(contact[0])})

@app.route('/contacts/api/1.0/contacts', methods=['POST'])
@auth.login_required
def post_contact():
    # require at least a name for a contact
    if not request.json or not 'name' in request.json:
        abort(400)
    new_contact = {
            'id': contacts[-1]['id'] + 1,
            'name': request.json['name'],
            'phone': request.json.get('phone', ""),
            'address': request.json.get('address', ""),
            'email': request.json.get('email', ""),
            'created_at': str(time.time()),
            'created_by': auth.username()
            }
    contacts.append(new_contact)
    return jsonify({'contact': make_contact_with_uri(new_contact)}), 201

@app.route('/contacts/api/1.0/contacts/<int:contact_id>', methods=['PUT'])
@auth.login_required
def update_contact(contact_id):
    protected = ['id', 'created_at', 'created_by','updated_at', 'updated_by']
    contact = [c for c in contacts if c['id'] == contact_id]
    for term in request.json:
        if term in protected:
            abort(405)
    if len(contact) == 0:
        abort(404)
    if not request.json:
        abort(400)
    for field in contact[0]:
        if field in request.json:
            contact[0][field] = request.json[field]
    contact[0]['updated_by'] = auth.username()
    contact[0]['updated_at'] = str(time.time())
    return jsonify({'contact': make_contact_with_uri(contact[0])}), 201

@app.route('/contacts/api/1.0/contacts/<int:contact_id>', methods=['DELETE'])
@auth.login_required
def delete_contact(contact_id):
    contact = [c for c in contacts if c['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    contacts.remove(contact[0])
    return jsonify({'contact':contact[0]}), 201

@app.route('/contacts/api/1.0/contacts/search', methods=['POST'])
def search_contacts():
    if not request.json or not 'terms' in request.json:
        abort(400)
    if len(request.json['terms']) > 1:
        abort(400)
    terms = request.json['terms']
    for term in terms:
        ret = [make_contact_with_uri(c) for c in contacts if c[term] == terms[term]]
    return jsonify({'contacts':ret}), 200

# ERROR HANDLING
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Not Allowed'}), 405)

# HELPERS
def make_contact_with_uri(contact):
    ret = {}
    for field in contact:
        if field == 'id':
            ret['uri'] = url_for('get_contact',
                    contact_id=contact['id'], _external=True)
        else:
            ret[field] = contact[field]
    return ret

if __name__ == '__main__':
    app.run(debug=True)
