import json
import base64
from app import app

class TestContactsApi:

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    # helper
    def open_with_auth(self, url, method, username, password, params):
        return self.app.open(url,
                method=method,
                headers={
                    'Authorization':'Basic ' + base64.b64encode(username + \
                            ":" + password)
                    },
                data=params,
                content_type='application/json'
                )

    # POST a new contact
    def test_it_should_require_authentication_to_modify_data(self):
        params = {'name':'Caleb Ewen'}
        result = self.app.post('/contacts/api/1.0/contacts', data=params)
        assert result.status_code == 401

    def test_it_should_400_if_not_provided_json_params(self):
        result = self.open_with_auth('/contacts/api/1.0/contacts', 'POST',
                'bomtoonen', 'password', 'test')
        assert result.status_code == 400

    def test_it_should_400_without_a_name(self):
        result = self.open_with_auth('/contacts/api/1.0/contacts', 'POST',
                'bomtoonen', 'password', {'test':'test'})
        assert result.status_code == 400

    def test_post_new_contact(self):
        params = json.dumps(dict(name='Caleb Ewen'))
        result = self.open_with_auth('/contacts/api/1.0/contacts', 'POST',
                'bomtoonen', 'password', params)
        assert result.status_code == 201
        index = self.app.get('/contacts/api/1.0/contacts')
        assert json.loads(index.data)['contacts'][-1]['name'] == 'Caleb Ewen'

    def test_it_should_remember_who_made_it(self):
        params = json.dumps(dict(name='Caleb Ewen'))
        result = self.open_with_auth('/contacts/api/1.0/contacts', 'POST',
                'bomtoonen', 'password', params)
        assert result.status_code == 201
        check = self.app.get('/contacts/api/1.0/contacts/2')
        assert json.loads(check.data)['contact']['created_by'] == 'bomtoonen'

    # GET an index of contacts
    def test_it_should_get_a_list_of_contacts(self):
        result = self.app.get('/contacts/api/1.0/contacts')
        assert result.status_code == 200

    def test_it_should_return_json(self):
        result = json.loads(self.app.get('/contacts/api/1.0/contacts').data)
        assert result['contacts'][0]['name'] == 'Peter Sagan'

    # it's nice to inclue the public uri for a subsequent GET instead of an id
    def test_record_should_include_public_uri(self):
        ret = json.loads(self.app.get('/contacts/api/1.0/contacts').data)
        expected_uri = 'http://localhost/contacts/api/1.0/contacts/1'
        assert ret['contacts'][0]['uri'] == expected_uri

    def test_it_shouldnt_worry_about_unnecessary_params_or_auth(self):
        params = json.dumps(dict(name='Caleb Ewen'))
        result = self.open_with_auth('/contacts/api/1.0/contacts', 'GET',
                'bomtoonen', 'password', params)
        assert result.status_code == 200

    # put search on its own endpoint so it can be a POST
    def test_it_should_filter_by_term(self):
        params = json.dumps(dict(terms=dict(name='Peter Sagan')))
        ret = self.open_with_auth('/contacts/api/1.0/contacts/search',
                'POST', 'bomtoonen', 'password', params)
        assert ret.status_code == 200
        assert len(json.loads(ret.data)['contacts']) == 1
        assert json.loads(ret.data)['contacts'][0]['name'] == 'Peter Sagan'

    # GET a contact by id
    def test_it_should_get_by_id(self):
        result = self.app.get('/contacts/api/1.0/contacts/1')
        assert result.status_code == 200
        assert json.loads(result.data)['contact']['name'] == 'Peter Sagan'

    def test_it_should_404_on_unknown_id(self):
        result = self.app.get('/contacts/api/1.0/contacts/404')
        assert result.status_code == 404
        assert json.loads(result.data)['error'] == 'Not Found'

    # UPDATE a contact by id
    def test_it_should_update_contact(self):
        params = json.dumps(dict(phone='1111111111'))
        result = self.open_with_auth('/contacts/api/1.0/contacts/1', 'PUT',
                'bomtoonen', 'password', params)
        assert result.status_code == 201
        check = self.app.get('/contacts/api/1.0/contacts/1')
        assert json.loads(check.data)['contact']['phone'] == '1111111111'

    def test_it_should_remember_who_touched_it(self):
        params = json.dumps(dict(phone='1111111111'))
        result = self.open_with_auth('/contacts/api/1.0/contacts/1', 'PUT',
                'bomtoonen', 'password', params)
        check = self.app.get('/contacts/api/1.0/contacts/1')
        assert json.loads(check.data)['contact']['updated_by'] == 'bomtoonen'

    def test_it_shouldnt_allow_update_of_protected_attrs(self):
        params = json.dumps(dict(id='42',
                                 updated_at='now',
                                 updated_by='Lance Armstrong',
                                 created_at='one second in the future',
                                 created_by='god'))
        ret = self.open_with_auth('/contacts/api/1.0/contacts/1', 'PUT',
                'bomtoonen', 'password', params)
        assert ret.status_code == 405
        check = self.app.get('/contacts/api/1.0/contacts/1')
        assert json.loads(check.data)['contact']['name'] == 'Peter Sagan'

    # DELETE a contact by id
    def test_it_should_require_authentication(self):
        ret = self.app.delete('/contacts/api/1.0/contacts/1')
        assert ret.status_code == 401

    def test_it_should_delete_the_requested_contact(self):
        ret = self.open_with_auth('/contacts/api/1.0/contacts/2',
                'DELETE', 'bomtoonen', 'password', params=None)
        assert ret.status_code == 201
        assert json.loads(ret.data)['contact']['name'] == 'Chris Froome'
        check = self.app.get('/contacts/api/1.0/contacts')
        assert len(json.loads(check.data)['contacts']) == 1

    def test_it_should_404_if_contact_not_found(self):
        ret = self.open_with_auth('/contacts/api/1.0/contacts/42',
                'DELETE', 'bomtoonen', 'password', params=None)
        assert ret.status_code == 404
