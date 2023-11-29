from flask import Flask, request
from flask_restful import Api, Resource
import subprocess
import logging

app = Flask(__name__)
api = Api(app)

class PathConfig(Resource):
    def post(self):

        router_id = request.form.get('router_id')
        router_type = request.form.get('router_type')
        path = request.form.get('path')

        if not router_id or not path:
            return {"error": "router_id and path are required"}, 400

        # command to add SRv6 route
        command = ""
        hostip = '192.168.1.207'
        if path == '1':
            command = f'route del {hostip}'
        elif path == '2':
            command = f'ip route add {hostip} encap seg6 mode encap segs fc00:2::da,fc00:3::da,fc00:4::da dev r1-eth3'
        elif path == '3':
            command = f'ip route add {hostip} encap seg6 mode encap segs fc00:5::5a,fc00:6::5a,fc00:4::5a dev r1-eth7'
        elif path == '4':
            command = f'ip route add {hostip} encap seg6 mode encap segs fc00:7::7a,fc00:8::7a,fc00:4::7a dev r1-eth9'
        else:
            return {"error": "Invalid path"}, 400

        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Command execution failed: {e}")
            return {"error": "Command execution failed"}, 500

        return {"info": f"Path {path} configured for router {router_id}"}, 200

api.add_resource(PathConfig, "/users")

if __name__ == "__main__":
    app.run(debug=True, host='10.0.0.2', port=7777)