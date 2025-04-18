```sh
controller01 $ sudo apt-get install python3-rbd ceph-common
controller01 $ sudo mkdir /etc/ceph

ceph-mon-01 $ sudo ceph osd pool create images 128
ceph-mon-01 $ sudo rbd pool init images

sudo ceph auth get-or-create client.glance   mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=images' -o /etc/ceph/ceph.client.glance.keyring
#OR
sudo ceph auth get-or-create client.glance   mon 'profile rbd' osd 'profile rbd pool=images' mgr 'profile rbd pool=images' -o /etc/ceph/ceph.client.glance.keyring

ceph-mon-01 $ sudo scp /etc/ceph/ceph.client.cinder.keyring root@controller01:/etc/ceph
controller01 $ sudo chgrp cinder /etc/ceph/ceph.client.cinder.keyring
controller01 $ sudo chmod 0640 /etc/ceph/ceph.client.cinder.keyring

ceph-mon-01 $ sudo vim /etc/ceph/ceph.conf
[client.images]
keyring = /etc/ceph/ceph.client.glance.keyring

controller01 $ sudo cp /etc/glance/glance-api.conf /etc/glance/glance-api.conf.orig

controller01 $ sudo vim /etc/glance/glance-api.conf
[glance_store]
stores = glance.store.rbd.Store,glance.store.http.Store
default_store = rbd
rbd_store_pool = images
rbd_store_user = glance
rbd_store_ceph_conf = /etc/ceph/ceph.conf
rbd_store_chunk_size = 8

show_image_direct_url = True

controller01 $ sudo systemctl restart glance-api.service

controller01 $ wget http://download.cirros-cloud.net/0.3.4/cirros-0.4.0-x86_64-disk.img
controller01 $ qemu-img convert cirros-0.4.0-x86_64-disk.img cirros-0.4.0-x86_64-disk.raw
controller01 $ glance image-create --name "Cirros-ceph1" --disk-format raw --container-format bare --visibility public --file cirros-0.4.0-x86_64-disk.raw
controller01 $ openstack image list

ceph-mon-01 $ sudo rbd ls images
ceph-mon-01 $ sudo rbd info images/a55e9417-67af-43c5-a342-85d2c4c483f7
```