#!/usr/bin/python

from pox.core import core 
import pox.openflow.libopenflow_01 as of 
from pox.lib.util import dpidToStr
import time

log = core.getLogger()

s0_dpid=0
s1_dpid=0
s2_dpid=0

def _handle_ConnectionUp (event):
	global s0_dpid, s1_dpid, s2_dpid
	print "ConnectionUp: ", dpidToStr(event.connection.dpid)

	#remember the connection dpid for switch
	for m in event.connection.features.ports:
		if m.name == "s0-eth1":
			s0_dpid = event.connection.dpid
			print "s0_dpid=", s0_dpid
		elif m.name == "s1-eth1":
			s1_dpid = event.connection.dpid
			print "s1_dpid=", s1_dpid
		elif m.name == "s2-eth1":
			s2_dpid = event.connection.dpid
			print "s2_dpid=", s2_dpid

def _handle_PacketIn (event):
	global s0_dpid, s1_dpid, s2_dpid
	print "PacketIn: ", dpidToStr(event.connection.dpid)
	if event.connection.dpid==s0_dpid:
		
		msg = of.ofp_flow_mod()
		msg.priority = 100	
		msg.match.in_port = 1
		msg.match.dl_type = 0x806 #arp reques
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)
		
		msg = of.ofp_flow_mod()
		msg.priority =100
		msg.match.in_port = 3
		msg.match.dl_type = 0x806 #arp request
		msg.actions.append(of.ofp_action_output(port = 1))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#ICMP request
		msg.priority = 1000	
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.3"
		msg.match.nw_proto = 1 #ICMPv4 request
		msg.actions.append(of.ofp_action_output(port = 1))
		event.connection.send(msg)
		
		msg = of.ofp_flow_mod() 		#ICMP request
		msg.priority = 1000		
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.2"
		msg.match.nw_proto = 1 #ICMPv4 request
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#ICMP request
		#!/usr/bin/pythonmsg.priority = 1000	
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.1"
		msg.match.nw_proto = 1 #ICMPv4 request
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#ANY
		msg.priority = 1000		
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.3"
		msg.actions.append(of.ofp_action_output(port = 1))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#UDP
		msg.priority = 1000		
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.1"
		msg.match.nw_proto = 17 #UDP
		msg.actions.append(of.ofp_action_output(port = 2))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#TCP
		msg.priority = 1000		
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.1"
		msg.match.nw_proto = 6 #TCP
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#TCP
		msg.priority = 1000		
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.2"
		msg.match.nw_proto = 6 #TCP
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)
	
	elif event.connection.dpid==s1_dpid:

		msg = of.ofp_flow_mod()
		msg.priority =1000
		msg.match.in_port = 1
		msg.actions.append(of.ofp_action_output(port = 2))
		event.connection.send(msg)
	
		msg = of.ofp_flow_mod()
		msg.priority =1000
		msg.match.in_port = 2
		msg.actions.append(of.ofp_action_output(port = 1))
		event.connection.send(msg)			

	elif event.connection.dpid==s2_dpid:
		msg = of.ofp_flow_mod()
		msg.priority =100
		msg.match.in_port = 2
		msg.match.dl_type = 0x806
		msg.actions.append(of.ofp_action_output(port = 3))  
		msg.actions.append(of.ofp_action_output(port = 4))
		event.connection.send(msg)

		msg = of.ofp_flow_mod()
		msg.priority = 100
		msg.match.in_port = 3
		msg.match.dl_type = 0x806
		msg.actions.append(of.ofp_action_output(port = 2))
		msg.actions.append(of.ofp_action_output(port = 4))
		event.connection.send(msg)

		msg = of.ofp_flow_mod()
		msg.priority =100
		msg.match.in_port = 4
		msg.match.dl_type = 0x806
		msg.actions.append(of.ofp_action_output(port = 2))
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#ANY
		msg.priority = 1000		
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.1"
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#ANY
		msg.priority = 1000		
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.2"
		msg.actions.append(of.ofp_action_output(port = 4))
		event.connection.send(msg)

		msg = of.ofp_flow_mod() 		#ANY
		msg.priority = 1000		
		msg.match.dl_type = 0x800 #Livello 3
		msg.match.nw_dst = "192.168.1.3"
		msg.actions.append(of.ofp_action_output(port = 2))
		event.connection.send(msg)

		
def launch ():
	core.openflow.addListenerByName("ConnectionUp",_handle_ConnectionUp)
	core.openflow.addListenerByName("PacketIn",_handle_PacketIn)
