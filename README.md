### Intent-aware SDN network adapation framework ###

This repo is an experimental framework of University of Surrey, EU-SPIRIT project.
Based on real-time application layer and transport layer trace, the SDN controller can decide whether to select a 
better path for incoming application flow.

Since research work based on this framework is still ongoing, the actual eBPF code, algorithm and topology will be
updated once this work can be published.

Some hardcoded parameter and testing code are remained in each module, will be updated later.


### Folders:

#### algorithm:
  + algo_data_collect_tcp.py: read output file capture by linux ss tool, save as pandas datatype
  + algo_data_parse_hologram.py: parse hologram output log file, save to .csv
  + algo_MAB.py: a collection of several popular MAB algorithms for further analysis of above data.

#### config:
  + config constants used in this project as .ini file

#### data: 
  + example test datas (e.g., tcp trace file, application layer trace file)

#### docs:
  + topology figures
  
#### ebpf_modules:
  + xdp kernel and user space to capture tcp packet information to given destination and export to user space.
  

#### rest_modules:
  - Restful server/client can be deployed on mininet nodes (e.g., r1, r4) 
  to exchange restful message to apply network adapation (e.g., route change)

#### scripts:
  - node_configuration: shell scripts to enable/disable functions on each node
  - ss_monitor.sh: generate tcp ss print from linux kernel and save to file

#### sdn_base:
  - sdn_http.py:  A class to create HTTP requests to a Ryu SDN controller REST server.
  - sdn_rest_dict.py: Stores all the GET requests

#### test:
  - testing basic functions

#### topo:
  - create_topo.py: create mininet topology and set path properties.
  - create_sdn_rules.py:  create and post SDN rules for switch.

