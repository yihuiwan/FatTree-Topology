from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller import ofp_event


class FlowRules(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FlowRules, self).__init__(*args, **kwargs)
        self.k = int(input('please input k: '))
        self.mac_to_port = {}

    def Dpid_Formalise(self, x):
        x = hex(x)
        x = x[2:]
        while len(x) != 6:
            x = '0' + x
        return x

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = self.Dpid_Formalise(datapath.id)

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # core sw
        if int(dpid[0]+dpid[1]) == self.k:
            for c in range(self.k):
                ip = '10.%d.0.0' % c
                mask = '255.255.0.0'
                out_port = c+1
                match = parser.OFPMatch(ipv4_dst=(ip, mask), eth_type=0x0800)
                actions = [parser.OFPActionOutput(out_port, 0)]
                self.add_flow(datapath, 10, match, actions)

        # ag sw
        elif int(dpid[2]+dpid[3]) >= self.k/2:
            for p in range(self.k):
                # prefix
                for s in range(int(self.k/2)):
                    # prefix
                    if int(dpid[0]+dpid[1]) == p:
                        ip = '10.%d.%d.0' % (p, s)
                        mask = '255.255.255.0'
                        out_port = int(s+self.k/2+1)
                        match = parser.OFPMatch(ipv4_dst=(ip, mask), eth_type=0x0800)
                        actions = [parser.OFPActionOutput(out_port, 0)]
                        self.add_flow(datapath, 10, match, actions)

                    # suffix
                    else:
                        ip = '0.0.0.%d' % (2+s)
                        mask = '0.0.0.255'
                        out_port = s+1
                        match = parser.OFPMatch(ipv4_dst=(ip, mask), eth_type=0x0800)
                        actions = [parser.OFPActionOutput(out_port, 0)]
                        self.add_flow(datapath, 1, match, actions)

        # ed sw
        else:
            for p in range(self.k):
                for s in range(int(self.k / 2)):
                    for h in range(2, 2+int(self.k / 2)):
                        # prefix
                        if int(dpid[0]+dpid[1]) == p and int(dpid[2]+dpid[3]) == s:
                            ip = '10.%d.%d.%d' % (p, s, h)
                            out_port = int(h+self.k/2-1)
                            match = parser.OFPMatch(ipv4_dst=ip, eth_type=0x0800)
                            actions = [parser.OFPActionOutput(out_port, 0)]
                            self.add_flow(datapath, 10, match, actions)

                        # suffix
                        else:
                            ip = '0.0.0.%d' % h
                            mask = '0.0.0.255'
                            out_port = h-1
                            match = parser.OFPMatch(ipv4_dst=(ip, mask), eth_type=0x0800)
                            actions = [parser.OFPActionOutput(out_port, 0)]
                            self.add_flow(datapath, 1, match, actions)
