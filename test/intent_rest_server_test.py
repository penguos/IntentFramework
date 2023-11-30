from flask import Flask, request
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

class IntentParser(Resource):
    def __init__(self):
        self.url = {
            'r4': 'http://10.0.2.2:7778/users',
            'r1': 'http://10.0.0.2:7777/users'
        }
        self.path = '1'

    def post_to_servers(self):
        headers = {'User-agent': f'ip config on {self.path}'}
        parms = {
            'router_id': 'Configure ip route',
            'router_type': 'ipv4' if self.path == '1' else 'srv6',
            'path': self.path
        }

        for key in self.url.keys():
            try:
                res = requests.post(self.url[key], data=parms, headers=headers)
                print(f'Response from {key}:', res.json())
            except requests.RequestException as e:
                print(f'Error during request to {self.url[key]}:', e)

class IntentParser_4K(IntentParser):
    def __init__(self):
        super().__init__()
        self.path = '1'

    def get(self):
        print("Receiving GET request for 4K")
        self.post_to_servers()
        return {"message": "Processed 4K request"}, 200

class IntentParser_2K(IntentParser):
    def __init__(self):
        super().__init__()
        self.path = '2'

    def get(self):
        print("Receiving GET request for 2K")
        self.post_to_servers()
        return {"message": "Processed 2K request"}, 200

api.add_resource(IntentParser_4K, "/Intent/Quality_Change/3840x2160")
api.add_resource(IntentParser_2K, "/Intent/Quality_Change/1080X720")

if __name__ == "__main__":
    wifi = 'WiFi_Home'
    hostip = '192.168.1.2' if wifi == 'WiFi_Home' else '192.168.1.8'

    app.run(debug=True, host=hostip, port=8082)
