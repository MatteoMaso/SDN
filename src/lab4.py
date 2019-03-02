#!/usr/bin/python lab4.py
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Controller
from mininet.cli import CLI

import os

class POXcontroller1( Controller):
	def start(self):
		self.pox='%s/pox/pox.py log.level --DEBUG > /tmp/pox.log' %os.environ['HOME']
		self.cmd(self.pox, "lab4_controller &")
	def stop(self):
		self.cmd('kill %' +self.pox)

controllers = { 'poxcontroller1': POXcontroller1}

class MyTopo(Topo):
	def __init__(self, n=2,**opts):
		Topo.__init__(self, **opts)
		s0 = self.addSwitch('s0')
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		h1=self.addHost('h1', cpu=.5/n)
		h2=self.addHost('h2', cpu=.5/n)
		h3=self.addHost('h3', cpu=.5/n)
		self.addLink(h1, s0, bw=10, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s0, s1, bw=10, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s0, s2, bw=10, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s1, s3, bw=10, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s2, s3, bw=10, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s3, h2, bw=10, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s3, h3, bw=10, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)

def perfTest():
	"Create network and run simple performance test"
	topo = MyTopo(n=3)
	net = Mininet(topo=topo,host=CPULimitedHost, link=TCLink,controller=POXcontroller1)
	net.start()
	print "Dumping host connections"
	dumpNodeConnections(net.hosts)
	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	perfTest()


