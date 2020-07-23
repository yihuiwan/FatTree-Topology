# FatTree-Topology and Ryu controller
use Mininet-python to create fattree topology and verify the topology by Ryu 

# How to use the code
1. Run Ryu in command window in Ryu director, use: PYTHONPATH=. ./bin/ryu run --observe-links ryu/app/gui_topology/gui_topology.py

2. Run Mininet in command window in ../mininet/custom director, use: sudo mn --custom FatTree.py --topo mytopo

     * notice that the code file should be in  ../mininet/custom director

3. Click on the Ryu link to view the topology in the browser (before that make sure the vm is connected to Internet)

# How to use Ryu controller
1. Run Ryu in command window in ../ryu/ryu/app director, use ryu-manager ryu_control.py

     * notice that the topology created mininet cannot be manipulated 2 Ryu controllers, i.e. the Ryu gui_topology function should be terminated while using this one
  
     * notice that the code file should be in  ../ryu/ryu/app director

2. Run Mininet in command window in ../mininet/custom director, use: sudo mn --custom fattree_topology.py --topo mytopo

     * use 'dpctl dump-flows' to check the flow rules
  
     * Use 'pingall' to test the reachablility of all ports
