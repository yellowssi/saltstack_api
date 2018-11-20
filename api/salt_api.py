import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SaltAPI:
    def __init__(self, ip_address, port, username, password):
        self.url = 'https://' + ip_address + ':' + str(port) + '/'
        self.headers = {
            'Content-type': 'application/json'
        }
        self.username = username
        self.password = password
        login_params = {
            'eauth': 'pam',
            'username': self.username,
            'password': self.password
        }
        token = self.get_data(self.url + 'login', login_params)['token']
        self.headers['X-Auth-Token'] = token

    def __del__(self):
        self.get_data(self.url + 'logout', {})

    def get_data(self, url, params):
        data = json.dumps(params)
        request = requests.post(url, data=data, headers=self.headers, verify=False)
        response = request.json()
        return dict(response)['return'][0]

    def list_all_key(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        response = self.get_data(self.url, params)
        result = {
            'accepted': response['data']['return']['minions'],
            'denied': response['data']['return']['minions_denied'],
            'unaccepted': response['data']['return']['minions_pre']
        }
        return result

    def accept_key(self, match):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': match}
        response = self.get_data(self.url, params)
        return response['data']['success']

    def delete_key(self, match):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': match}
        response = self.get_data(self.url, params)
        return response['data']['success']

    def salt_cmd(self, tgt, fun, args=None):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        if args:
            params['arg'] = args
        return self.get_data(self.url, params)

    def salt_async_cmd(self, tgt, fun, args=None):
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun}
        if args:
            params['arg'] = args
        return self.get_data(self.url, params)

    def compound_cmd(self, tgt, fun, args=None):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'expr_form': 'compound'}
        if args:
            params['arg'] = args
        return self.get_data(self.url, params)

    def compound_async_cmd(self, tgt, fun, args=None):
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'expr_form': 'compound'}
        if args:
            params['arg'] = args
        return self.get_data(self.url, params)

    def group_cmd(self, tgt, fun, args=None):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'expr_form': 'nodegroup'}
        if args:
            params['arg'] = args
        return self.get_data(self.url, params)

    def salt_run(self, tgt, fun, args=None):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'expr_form': 'compound'}
        if args:
            params['arg'] = params
        return self.get_data(self.url + 'run', params)

    def get_jid_ret(self, jid):
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        return self.get_data(self.url, params)

    def list_running_jobs(self):
        params = {'client': 'runner', 'fun': 'jobs.active'}
        return self.get_data(self.url, params)

    def get_job_status(self, jid):
        return requests.get(self.url + 'jobs/' + jid)
