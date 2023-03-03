



## Ryu



* Start mininet

```bash
ubuntu@sdnhubvm:~[21:47]$ sudo mn --top single,3 --mac --controller remote --switch ovsk
```



* Start Ryu with custom code

```bash
ubuntu@sdnhubvm:~/ryu[21:47] (master)$ pwd
/home/ubuntu/ryu
ubuntu@sdnhubvm:~/ryu[21:47] (master)$ bin/ryu-manager --verbose ../hojat/Learning_Switch/simple_switch_13.py
```



* Test connectons

```bash
mininet> h1 ping h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=15.1 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.570 ms
^C
--- 10.0.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.570/7.858/15.146/7.288 ms
mininet> h2 ping h3
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=13.3 ms
^C
--- 10.0.0.3 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 13.349/13.349/13.349/0.000 ms
mininet> 

```

