## Create networks on contrller


### Create the provider network
```shell
. admin-openrc

openstack network create  --share --external \
  --provider-physical-network provider \
  --provider-network-type flat provider

openstack subnet create --network provider \
  --allocation-pool start=172.16.55.101,end=172.16.55.150 \
  --dns-nameserver 8.8.4.4 --gateway 172.16.55.254 \
  --subnet-range 172.16.55.0/24 provider

```
### Self-service network
```shell

openstack network create selfservice

openstack subnet create --network selfservice \
  --dns-nameserver 8.8.4.4 --gateway 172.16.1.1 \
  --subnet-range 172.16.1.0/24 selfservice

openstack router create router
openstack router add subnet router selfservice
openstack router set router --external-gateway provider

```
### Verify operation
```shell

controller$ ip netns

openstack port list --router router


```
