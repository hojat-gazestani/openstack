## Ryu simple L3 switch verbos mode

* L3 switch source code name is "simple_switch_13_3_verbose.py"

[L3 switch source code](path)

* Run mininet

```bash
ubuntu@sdnhubvm:~[23:37]$ history sudo mn --top single,3 --mac --controller remote --switch ovsk
```



* Run the ryu manager with the source code

```bash
ubuntu@sdnhubvm:~[01:05]$ ./ryu/bin/ryu-manager ./hojat/Learning_Switch/simple_switch_13_3_verbose.py
```



* ping for first time

```bash
mininet> h1 ping -c 1  h3
```



* Verbose mode showing the flow is creating at the controller

```ba
msg: version: 0x4 msg_type 0xa xid 0x0 OFPPacketIn(buffer_id=256,cookie=0,data='\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x02\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01\x00\x00\x00\x00\x00\x02\n\x00\x00\x02\x00\x00\x00\x00\x00\x00\n\x00\x00\x03',match=OFPMatch(oxm_fields={'in_port': 2}),reason=0,table_id=0,total_len=42)
datapath: <ryu.controller.controller.Datapath object at 0x7ffd3f1e4490>
ofproto: <module 'ryu.ofproto.ofproto_v1_3' from '/home/ubuntu/ryu/ryu/ofproto/ofproto_v1_3.pyc'>
parser: <module 'ryu.ofproto.ofproto_v1_3_parser' from '/home/ubuntu/ryu/ryu/ofproto/ofproto_v1_3_parser.pyc'>
in_port: 2
pkt: ethernet(dst='ff:ff:ff:ff:ff:ff',ethertype=2054,src='00:00:00:00:00:02'), arp(dst_ip='10.0.0.3',dst_mac='00:00:00:00:00:00',hlen=6,hwtype=1,opcode=1,plen=4,proto=2048,src_ip='10.0.0.2',src_mac='00:00:00:00:00:02')
eth: ethernet(dst='ff:ff:ff:ff:ff:ff',ethertype=2054,src='00:00:00:00:00:02')
dst: ff:ff:ff:ff:ff:ff
src: 00:00:00:00:00:02
dpid: 1
packet in 1 00:00:00:00:00:02 ff:ff:ff:ff:ff:ff 2
out_port: 4294967291
actions: [OFPActionOutput(len=16,max_len=65509,port=4294967291,type=0)]
out: version: None msg_type None xid None OFPPacketOut(actions=[OFPActionOutput(len=16,max_len=65509,port=4294967291,type=0)],actions_len=0,buffer_id=256,data=None,in_port=2)
msg: version: 0x4 msg_type 0xa xid 0x0 OFPPacketIn(buffer_id=257,cookie=0,data='\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x03\x08\x06\x00\x01\x08\x00\x06\x04\x00\x02\x00\x00\x00\x00\x00\x03\n\x00\x00\x03\x00\x00\x00\x00\x00\x02\n\x00\x00\x02',match=OFPMatch(oxm_fields={'in_port': 3}),reason=0,table_id=0,total_len=42)
datapath: <ryu.controller.controller.Datapath object at 0x7ffd3f1e4490>
ofproto: <module 'ryu.ofproto.ofproto_v1_3' from '/home/ubuntu/ryu/ryu/ofproto/ofproto_v1_3.pyc'>
parser: <module 'ryu.ofproto.ofproto_v1_3_parser' from '/home/ubuntu/ryu/ryu/ofproto/ofproto_v1_3_parser.pyc'>
in_port: 3
pkt: ethernet(dst='00:00:00:00:00:02',ethertype=2054,src='00:00:00:00:00:03'), arp(dst_ip='10.0.0.2',dst_mac='00:00:00:00:00:02',hlen=6,hwtype=1,opcode=2,plen=4,proto=2048,src_ip='10.0.0.3',src_mac='00:00:00:00:00:03')
eth: ethernet(dst='00:00:00:00:00:02',ethertype=2054,src='00:00:00:00:00:03')
dst: 00:00:00:00:00:02
src: 00:00:00:00:00:03
dpid: 1
packet in 1 00:00:00:00:00:03 00:00:00:00:00:02 3
out_port: 2
actions: [OFPActionOutput(len=16,max_len=65509,port=2,type=0)]
match: OFPMatch(oxm_fields={'eth_dst': '00:00:00:00:00:02', 'in_port': 3})
mod: version: None msg_type None xid None OFPFlowMod(buffer_id=257,command=0,cookie=0,cookie_mask=0,flags=0,hard_timeout=0,idle_timeout=0,instructions=[OFPInstructionActions(actions=[OFPActionOutput(len=16,max_len=65509,port=2,type=0)],type=4)],match=OFPMatch(oxm_fields={'eth_dst': '00:00:00:00:00:02', 'in_port': 3}),out_group=0,out_port=0,priority=1,table_id=0)
msg: version: 0x4 msg_type 0xa xid 0x0 OFPPacketIn(buffer_id=258,cookie=0,data='\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x02\x08\x00E\x00\x00T]g@\x00@\x01\xc9=\n\x00\x00\x02\n\x00\x00\x03\x08\x00\xfe\x18\x1a\xb8\x00\x01T\xbe\x01d\x00\x00\x00\x00\xbf8\x0b\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567',match=OFPMatch(oxm_fields={'in_port': 2}),reason=0,table_id=0,total_len=98)
datapath: <ryu.controller.controller.Datapath object at 0x7ffd3f1e4490>
ofproto: <module 'ryu.ofproto.ofproto_v1_3' from '/home/ubuntu/ryu/ryu/ofproto/ofproto_v1_3.pyc'>
parser: <module 'ryu.ofproto.ofproto_v1_3_parser' from '/home/ubuntu/ryu/ryu/ofproto/ofproto_v1_3_parser.pyc'>
in_port: 2
pkt: ethernet(dst='00:00:00:00:00:03',ethertype=2048,src='00:00:00:00:00:02'), ipv4(csum=51517,dst='10.0.0.3',flags=2,header_length=5,identification=23911,offset=0,option=None,proto=1,src='10.0.0.2',tos=0,total_length=84,ttl=64,version=4), icmp(code=0,csum=65048,data=echo(data='T\xbe\x01d\x00\x00\x00\x00\xbf8\x0b\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567',id=6840,seq=1),type=8)
eth: ethernet(dst='00:00:00:00:00:03',ethertype=2048,src='00:00:00:00:00:02')
dst: 00:00:00:00:00:03
src: 00:00:00:00:00:02
dpid: 1
packet in 1 00:00:00:00:00:02 00:00:00:00:00:03 2
out_port: 3
actions: [OFPActionOutput(len=16,max_len=65509,port=3,type=0)]
match: OFPMatch(oxm_fields={'eth_dst': '00:00:00:00:00:03', 'in_port': 2})
mod: version: None msg_type None xid None OFPFlowMod(buffer_id=258,command=0,cookie=0,cookie_mask=0,flags=0,hard_timeout=0,idle_timeout=0,instructions=[OFPInstructionActions(actions=[OFPActionOutput(len=16,max_len=65509,port=3,type=0)],type=4)],match=OFPMatch(oxm_fields={'eth_dst': '00:00:00:00:00:03', 'in_port': 2}),out_group=0,out_port=0,priority=1,table_id=0)
```



* Showing the flow on the controller

```bash
ubuntu@sdnhubvm:~[01:37]$ sudo ovs-ofctl dump-flows s1
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=378.751s, table=0, n_packets=4, n_bytes=280, idle_age=373, priority=1,in_port=3,dl_dst=00:00:00:00:00:02 actions=output:2
 cookie=0x0, duration=378.739s, table=0, n_packets=3, n_bytes=238, idle_age=373, priority=1,in_port=2,dl_dst=00:00:00:00:00:03 actions=output:3
 cookie=0x0, duration=223.813s, table=0, n_packets=7, n_bytes=462, idle_age=148, priority=1,in_port=3,dl_dst=00:00:00:00:00:01 actions=output:1
 cookie=0x0, duration=223.807s, table=0, n_packets=6, n_bytes=420, idle_age=148, priority=1,in_port=1,dl_dst=00:00:00:00:00:03 actions=output:3
 cookie=0x0, duration=382.967s, table=0, n_packets=24, n_bytes=1120, idle_age=223, priority=0 actions=CONTROLLER:65535

```



* And if you ping again find it connection is stablished without creating new flow on controller, Because the flow existed before

