## Launch Instance on contrller

```shell
. admin-openrc

openstack flavor create --id 0 --vcpus 1 --ram 64 --disk 1 m1.nano


. demo-openrc 

ssh-keygen -q -N ""
openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey

openstack keypair list

openstack security group rule create --proto icmp default
openstack security group rule create --proto tcp --dst-port 22 default
```

### Launch an instance on the provider network

```shell
 . demo-openrc

openstack flavor list
openstack image list
openstack network list
openstack security group list

openstack server create --flavor m1.nano --image cirros \
  --nic net-id=fb091613-8249-4cfa-90d5-04fa9acc31d4 --security-group default \
  --key-name mykey provider-in

openstack server list

openstack console url show provider-instanc

ping -c 4 203.0.113.1

ping -c 4 openstack.org
```

* Access the instance remotely
----------------------------
```shell
ping -c 4 203.0.113.103
ssh cirros@203.0.113.103
```

* Launch an instance on the self-service network
----------------------------------------------
```shell

. demo-openrc

openstack flavor list
openstack image list
openstack network list
openstack security group list

openstack server create --flavor m1.nano --image cirros \
  --nic net-id=SELFSERVICE_NET_ID --security-group default \
  --key-name mykey selfservice-instance

openstack server list
```
* Access the instance using a virtual console
-------------------------------------------
```shell
openstack console url show selfservice-instance
ping -c 4 172.16.1.1
ping -c 4 openstack.org
```

* Access the instance remotely
----------------------------
```shell
openstack floating ip create provider
openstack server add floating ip selfservice-instance 203.0.113.104

openstack server list

ping -c 4 203.0.113.104

ssh cirros@203.0.113.104
```


------------------------
```shell
openstack server create \
--flavor m1.nano \
--image cirros \
--nic net-id=3d7b6090-ce13-4598-80c5-edb92e01d198  \
--security-group 7332400f-b17f-469b-b4fd-c65a54b5e53f \
--key-name mykey \
--availability-zone nova:compute01 \
selfservice-instance
```
