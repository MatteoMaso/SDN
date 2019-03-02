#Spedisci i flussi dati UDP e TCP
#!/usr/bin/python
from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log  import setLogLevel
from mininet.node import Controller
from mininet.cli  import CLI
from functools    import partial
import time
import os
class POXcontroller1( Controller):
	def start(self):
		self.pox='%s/pox/pox.py ' %os.environ['HOME']
		self.cmd(self.pox, "project_controller &")

	def stop(self):
		self.cmd('kill %' +self.pox)

controllers = { 'poxcontroller1': POXcontroller1}


class MyTopo(Topo):
	def __init__(self, n=2,**opts):
		Topo.__init__(self, **opts)
		s0 = self.addSwitch('s0')
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		h0=self.addHost('h0', cpu=.5/n)
		h1=self.addHost('h1', cpu=.5/n)
		h2=self.addHost('h2', cpu=.5/n)
		self.addLink(h0, s0, bw=10, delay='50ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s0, s2, bw=2, delay='20ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s0, s1, bw=1, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s1, s2, bw=1, delay='10ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s2, h1, bw=5, delay='20ms',loss=0, max_queue_size=1000, use_htb=True)
		self.addLink(s2, h2, bw=5, delay='20ms',loss=0, max_queue_size=1000, use_htb=True)

def perfTest():
    		#Crea la rete e assegna gli indirizzi IP
		topo = MyTopo(n=3)
	    	net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=POXcontroller1)
	    	net.start()
		h0, h1, h2 = net.get('h0', 'h1', 'h2')
		h0.setIP( '192.168.1.3/24' )
		h1.setIP( '192.168.1.1/24' )
		h2.setIP( '192.168.1.2/24' )
		
		#Testa la connettivita' della rete
		print "Dumping host connections"
		dumpNodeConnections(net.hosts)
		print "Testing network connectivity"
		net.pingAll()
		
		#Attiva i ricevitori
		print "Starting simulation"
		h1.cmd('iperf -s -u -i 2 > ./udp_traffic0.txt &')       #ascolta UDP in arrivo
		h1.cmd('iperf -s -i 2    > ./tcp_traffic1.txt &')	#ascolta TCP1 in arrivo
		h2.cmd('iperf -s -i 2    > ./tcp_traffic2.txt &')	#ascolta TCP2 in arrivo
		
		#Spedisci i flussi dati UDP e TCP
		
		print h0.cmd('iperf -c 192.168.1.1 -n 6000K &')         #carica TCP1
		print h0.cmd('iperf -c 192.168.1.2 -n 6000K &')		#carica TCP2
		time.sleep(4)
		print h0.cmd('iperf -c 192.168.1.1 -u -n 2000K ')  	#carica UDP
		time.sleep(60)		

		#Kill iperf and print data
		h0.cmd('kill %iperf')
		h1.cmd('kill %iperf')
		h2.cmd('kill %iperf')
		f=open('./udp_traffic0.txt')
		lineno=1
		for line in f.readlines():
			print "%d: %s" % (lineno, line.strip())
			lineno+=1
		f=open('./tcp_traffic1.txt')
		lineno=1
		for line in f.readlines():
			print "%d: %s" % (lineno, line.strip())
			lineno+=1
		f=open('./tcp_traffic2.txt')
		lineno=1
		for line in f.readlines():
			print "%d: %s" % (lineno, line.strip())
			lineno+=1
		CLI(net)
		net.stop()

if __name__ == '__main__':
		setLogLevel('info')
		perfTest()


