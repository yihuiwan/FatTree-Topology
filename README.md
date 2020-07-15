# FatTree-Topology
use Mininet-python to create fattree topology and verify the topology by Ryu 

# How to use the code
1. Run Ryu in command window, use: PYTHONPATH=. ./bin/ryu run --observe-links ryu/app/gui_topology/gui_topology.py

2. Run Mininet in command window, use: sudo mn --custom test.py --topo mytopo

3. Click on the Ryu link to view the topology in the browser (before that make sure the vm is connected to Internet)

# next time I will focus on how to use Ryu controller
