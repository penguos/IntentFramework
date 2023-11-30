from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
from datetime import datetime
import sys
sys.path.append('../')
from config.config_parser import app_config

app = Flask(__name__)
api = Api(app)

# set parameters to parse
parser_put = reqparse.RequestParser()
parser_put.add_argument("content_provider", type=str, required=True, help="need content provider")
parser_put.add_argument("resolution", type=str, required=True, help="need resolution")
parser_put.add_argument("path", type=str, help="need path")

logPath = app_config.get("General","logPath")
remotePath = app_config.get("General","remotePath")
sdn_event_log = 'sdn_event_log.txt'

class IntentParser(Resource):
    def post_request(self, url, parms, headers):
        try:
            response = requests.post(url, data=parms, headers=headers)
            return response.json()
        except requests.RequestException as e:
            print(f"Error during request to {url}: {e}")
            return None
    def change_path(self, path):
        urls = {
            "r4": "http://10.0.2.2:7778/users",
            "r1": "http://10.0.0.2:7777/users"
        }
        router_type = 'ipv4' if path == '1' else 'srv6'
        parms = {
            'router_id': 'Configure ip route',
            'router_type': router_type,
            'path': path
        }
        headers = {'User-agent': f'ip config on {path}'}

        for key in urls:
            response = self.post_request(urls[key], parms, headers)
            print(response)

    def get(self):
        args = parser_put.parse_args()
        path = args['path']

        if path not in ['1', '11', '2']:
            return {"error": "Invalid path"}, 400

        self.change_path(path)
        return {"message": f"Path {path} changed"}, 200

# add restful path resource
api.add_resource(IntentParser, "/Intent/Quality_Change/3840x2160")

if __name__ == "__main__":
    hostip = app_config.get("General","local_server_ip")
    app.run(debug=True, host=hostip, port=8082)
