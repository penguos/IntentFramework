import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from config.config_parser import app_config
import collections
from backup.sdn_http import SdnRequests
from sdn_base.sdn_rest_dict import sdn_update_the_switch_stats as sdn_post

def generate_sdn_rules(dpid, ports, controller_ip, table_id, priority):
    """
    Generate and post SDN rules for  switch.
    """
    rules = collections.defaultdict(list)

    for i, switch in enumerate(dpid):
        sw_id = int(list(switch.values())[0])
        in_ports = list(ports[i].keys())
        out_ports = [val for val in ports[i].values()]

        for in_port, out_port in zip(in_ports, out_ports):
            print(f"Switch ID: {sw_id}, In-port: {in_port}, Out-port: {out_port}")
            rule = {
                "dpid": sw_id,
                "table_id": table_id,
                "priority": priority,
                "match": {"in_port": in_port},
                "actions": [{"type": "OUTPUT", "port": out_port}]
            }
            rules[sw_id].append(rule)

            # Post the rule to the SDN controller
            try:
                req = SdnRequests(ip=controller_ip, rest_api=sdn_post['Add_a_flow_entry'])
                response = req.post(rule)
                if response:
                    print(f"Rule posted successfully for switch {sw_id}.")
                else:
                    print(f"Failed to post rule for switch {sw_id}.")
            except Exception as e:
                print(f"Error posting rule for switch {sw_id}: {e}")

    return rules


if __name__ == "__main__":
    # Define switches and ports
    dpid = [{'s11': 11}, {'s22': 22}]
    s11_ports = {11: 2, 2: 11, 12: 3, 3: 12, 13: 4, 4: 13, 14: 5, 5: 14, 15: 6, 6: 15, 7: 16, 16: 7}
    s22_ports = {7: 2, 2: 7, 1: 3, 3: 1, 4: 6, 6: 4, 8: 5, 5: 8, 10: 9, 9: 10}
    ports = [s11_ports, s22_ports]
    # Generate and post SDN rules
    controller_ip = app_config.get("General", "controller_ip")
    table_id = 0
    priority = 1000
    rules = generate_sdn_rules(dpid, ports, controller_ip, table_id, priority)

    print(f"Total number of rules generated: {sum(len(rules[sw]) for sw in rules)}")
