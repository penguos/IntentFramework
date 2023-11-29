import requests
import collections

from sdn_base.sdn_rest_dict import sdn_retrieve_the_switch_stats as sdn_get
from sdn_base.sdn_rest_dict import sdn_update_the_switch_stats as sdn_post

class SdnRequests:
    """
    A class to create HTTP requests to a Ryu SDN controller REST server.
    """

    def __init__(self, ip=None, port='8080', rest_api='', dpid=''):
        # Initialize URLs for GET, POST, and DELETE requests
        self.urlGet = f'http://{ip}:{port}{rest_api}{dpid}'
        self.urlPost = f'http://{ip}:{port}{rest_api}'
        self.urlDelete = f'http://{ip}:{port}/stats/flowentry/clear/{dpid}'

    def get(self):
        """
        Perform a GET request to the SDN controller.
        """
        try:
            response = requests.get(self.urlGet)
            response.raise_for_status()  # Raise exception for HTTP error responses
            return response.json()  # Return JSON response
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
        return None

    def post(self, data):
        """
        Perform a POST request to the SDN controller.
        """
        try:
            response = requests.post(self.urlPost, json=data)
            response.raise_for_status()  # Raise exception for HTTP error responses
            return response.json()  # Return JSON response
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
        return None

    def clear(self, dpid):
        """
        Perform a DELETE request to clear flows from the SDN switch.
        """
        try:
            response = requests.delete(self.urlDelete)
            response.raise_for_status()  # Raise exception for HTTP error responses
            return response.json()  # Return JSON response
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
        return None

# Example usage
if __name__ == '__main__':
    # Define the SDN switches and corresponding ports
    dpid = [{'s11': 11}, {'s22': 22}]
    ports = [{1: 2, 2: 1}, {1: 2, 2: 1}]  # Example port mappings for s11 and s22

    controller_ip = 'localhost'
    rest_method = "POST"

    if rest_method == 'GET':
        for switch in dpid:
            sw_id = list(switch.values())[0]
            sw_ports = ports[dpid.index(switch)]
            for in_port in sw_ports:
                req = SdnRequests(ip=controller_ip, rest_api=sdn_get['Get_ports_stats'], dpid=f'{sw_id}/{in_port}')
                response = req.get()
                if response:
                    print(f'GET response for switch {sw_id}, port {in_port}: {response}')
                else:
                    print(f'Failed to get response for switch {sw_id}, port {in_port}')

    elif rest_method == 'DELETE':
        sw_id = list(dpid[0].values())[0]
        req = SdnRequests(ip=controller_ip, dpid=str(sw_id))
        response = req.clear(sw_id)
        if response:
            print(f'DELETE response for switch {sw_id}: {response}')
        else:
            print(f'Failed to delete flows for switch {sw_id}')

    elif rest_method == 'POST':
        for switch in dpid:
            sw_id = list(switch.values())[0]
            sw_ports = ports[dpid.index(switch)]
            for in_port, out_port in sw_ports.items():
                rule = {
                    "dpid": sw_id,
                    "table_id": 0,  # Example table ID
                    "priority": 1000,  # Example priority
                    "match": {"in_port": in_port},
                    "actions": [{"type": "OUTPUT", "port": out_port}]
                }
                req = SdnRequests(ip=controller_ip, rest_api=sdn_post['Add_a_flow_entry'])
                response = req.post(rule)
                if response:
                    print(f'POST response for switch {sw_id}, rule {rule}: {response}')
                else:
                    print(f'Failed to post rule for switch {sw_id}, rule {rule}')
