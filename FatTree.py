#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import Link, Intf, TCLink
from mininet.node import Controller,OVSSwitch,RemoteController,CPULimitedHost
from mininet.cli import CLI


class FatTree(Topo):
    def __init__(self):
        Topo.__init__(self)
        self.k = int(input('please input k: '))
        self.PortNum, self.PodNum = self.k, self.k
        self.CoreNum = int(pow(self.k/2, 2))
        self.CoreName = ['c'+str(x) for x in range(self.CoreNum)]
        self.AggrNum = int(self.k / 2 * self.PodNum)
        self.AggrName = ['a'+str(x) for x in range(self.AggrNum)]
        self.EdgeNum = int(self.k / 2 * self.PodNum)
        self.EdgeName = ['e'+str(x) for x in range(self.EdgeNum)]
        self.HostNum = int(pow(self.k, 3)/4)
        self.HostName = ['h'+str(x) for x in range(self.HostNum)]

        self.HList = []
        self.CsList = []
        self.AsList = []
        self.EsList = []

        self.CreatSwitch()
        self.CreatHost()
        self.Addlinks()

    def CreatSwitch(self):
        # core
        count = 0
        for i in range(int(self.k/2)):
            for j in range(int(self.k/2)):
                dpid = "00:00:00:00:00:%02d:%02d:%02d" % (self.k, j, i)
                self.CsList.append(self.addSwitch(str(self.CoreName[count]), dpid=dpid))
                count += 1
        # Aggregation
        count = 0
        for p in range(self.PodNum):
            for s in range(int(self.k / 2), self.k):
                dpid = "00:00:00:00:00:%02d:%02d:01" % (p, s)
                self.AsList.append(self.addSwitch(str(self.AggrName[count]), dpid=dpid))
                count += 1
        # Edge
        count = 0
        for p in range(self.PodNum):
            for s in range(int(self.k / 2)):
                dpid = "00:00:00:00:00:%02d:%02d:01" % (p, s)
                self.EsList.append(self.addSwitch(str(self.EdgeName[count]), dpid=dpid))
                count += 1

    def CreatHost(self):
        count = 0
        for p in range(self.PodNum):
            for s in range(int(self.k / 2)):
                for i in range(2, int(self.k/2)+2):
                    ip = '10.%d.%d.%d' % (p, s, i)
                    self.HList.append(self.addHost(str(self.HostName[count]), ip=ip))
                    count += 1

    def Addlinks(self):
        # core - aggr
        GroupNum = int(self.AggrNum / self.PodNum)
        for i in range(self.CoreNum):
            GroupNo = int(i // GroupNum)
            for j in range(self.AggrNum):
                if j % GroupNum == GroupNo:
                    self.addLink(self.CsList[i], self.AsList[j])

        # aggr - edge
        for i in range(self.AggrNum):
            PodNo = int(i // GroupNum)
            for j in range(GroupNum*PodNo, GroupNum*(PodNo+1)):
                self.addLink(self.AsList[i], self.EsList[j])

        # edge - host
        for i in range(self.EdgeNum):
            for j in range(i*GroupNum, (i+1)*GroupNum):
                self.addLink(self.EsList[i], self.HList[j])


def CreatNet():
    topo = FatTree()
    net = Mininet(topo=topo, controller=None, autoSetMacs=True, autoStaticArp=True, host=CPULimitedHost, link=TCLink)
    net.addController('controller', controller=RemoteController, ip='127.0.0.1', port=6633, protocols="OpenFlow13")
    net.start()
    CLI(net)
    net.stop()


topos = {'mytopo': (lambda: CreatNet())}
