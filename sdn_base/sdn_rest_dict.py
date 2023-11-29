# Stores all the GET requests
sdn_retrieve_the_switch_stats = {
    'Get_all_switches': '/stats/switches',
    'Get_desc_stats': '/stats/desc/',
    'Get_all_flows_stats': '/stats/flow/',
    'Get_table_stats': '/stats/table/',
    'Get_table_features': '/stats/tablefeatures/',
    'Get_ports_stats': '/stats/port/',
    'Get_ports_description': '/stats/portdesc/',
    'Get_queues_stats': '/stats/queue/',
    'Get_queues_config': '/stats/queueconfig/',
    'Get_group_stats': '/stats/group/',
    'Get_meters_stats': '/stats/meter/',
    'Get_meter_config': '/stats/meterconfig/',
    'Get_meter_features_stats': '/stats/meterfeatures/',
    'Get_role': '/stats/role/'
}

# stores all the POST requests
sdn_update_the_switch_stats = {
    'Add_a_flow_entry': '/stats/flowentry/add',
    'Modify_all_matching_flow_entries': '/stats/flowentry/modify',
    'Modify_flow_entry_strictly': '/stats/flowentry/modify_strict',
    'Delete_all_matching_flow_entries': '/stats/flowentry/delete',
    'Delete_flow_entry_strictly': '/stats/flowentry/delete_strict',
    'Add_a_meter_entry': '/stats/meterentry/add',
    'Modify_a_meter_entry': '/stats/meterentry/modify',
    'Delete_a_meter_entry': '/stats/meterentry/delete',
    'Modify_role': '/stats/role'
}


# stores all the Monitoring stats to be stored/retrived
monitor_stats = ('actions',
               'idle_timeout',
               'cookie',
               'packet_count',
               'hard_timeout',
               'byte_count',
               'duration_sec',
               'duration_nsec',
               'priority',
               'length',
               'flags',
               'table_id',
               'match')

