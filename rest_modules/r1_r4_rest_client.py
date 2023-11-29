import requests

class Path_Request:
    def __init__(self, path_id):
        self.path_id = path_id
        self.url = {'r4': 'http://10.0.2.2:7778/users', 'r1': 'http://10.0.0.2:7777/users'}
        self.router_id = 'Configure ip route'
        self.router_type = 'srv6'
        self.user_agent = {'r4': 'ip config on 10.0.2.2', 'r1': 'ip config on 10.0.0.2'}

    def get_path_params(self):
        return {'router_id': self.router_id, 'router_type': self.router_type, 'path': self.path_id}

    def get_url(self, router_id):
        return self.url[router_id]

    def get_headers(self, router_id):
        return {'User-agent': self.user_agent[router_id]}

def path_change_test(path_id):
    mod_path = Path_Request(path_id)

    try:
        res_r1 = requests.post(mod_path.get_url('r1'), data=mod_path.get_path_params(),
                               headers=mod_path.get_headers('r1'))
        res_r4 = requests.post(mod_path.get_url('r4'), data=mod_path.get_path_params(),
                               headers=mod_path.get_headers('r4'))

        print('Response from r1:')
        print('Status Code:', res_r1.status_code)
        print('Response Body:', res_r1.json())

        print('\nResponse from r4:')
        print('Status Code:', res_r4.status_code)
        print('Response Body:', res_r4.json())

    except requests.exceptions.RequestException as e:
        print('Error during requests to servers:', e)

if __name__ == "__main__":
    path_change_test(3)
