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

        # add route according to path index
        command = ""
        if path == '1':
            command = 'route del 10.0.0.101'
        elif path == '2':
            command = 'ip route add 10.0.0.101 encap seg6 mode encap segs fc00:3::dd,fc00:2::dd,fc00:1::dd dev r4-eth2'
        elif path == '3':
            command = 'ip route add 10.0.0.101 encap seg6 mode encap segs fc00:6::dd,fc00:5::dd,fc00:1::dd dev r4-eth6'
        elif path == '4':
            command = 'ip route add 10.0.0.101 encap seg6 mode encap segs fc00:9::dd,fc00:9::dd,fc00:9::dd dev r4-eth10'
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
    app.run(debug=True, host='10.0.2.2', port=7778)
