# Initial Ceph polls and auth

```sh
controller01 {glance-api} $ sudo apt-get install python3-rbd python3-rados
controller01 {glance-api}  / compute-node {nova-compute} / block-storage {cinder-backup+cinder-volume} $ sudo apt-get install ceph-common

controller01 / block / compute $ sudo mkdir /etc/ceph

ceph-mon-01 $ sudo ceph osd pool create volumes 128
ceph-mon-01 $ sudo ceph osd pool create images 128
ceph-mon-01 $ sudo ceph osd pool create backups 128
ceph-mon-01 $ sudo ceph osd pool create vms 128
ceph-mon-01 $ sudo ceph osd lspools

ceph-mon-01 $ sudo rbd pool init volumes
ceph-mon-01 $ sudo rbd pool init images
ceph-mon-01 $ sudo rbd pool init backups
ceph-mon-01 $ sudo rbd pool init vms

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
client.glance   mon 'allow r' 
		osd 'allow class-read object_prefix rbd_children, allow rwx pool=images'

client.glance   mon 'profile rbd' 
		osd 'profile rbd pool=images' 
		mgr 'profile rbd pool=images'

ceph-mon-01 $ scp /etc/ceph/ceph.conf root@controller01:/etc/ceph
ceph-mon-01 $ scp /etc/ceph/ceph.client.glancekeyring  root@controller01:/etc/ceph
#OR
ceph-mon-01 $ ceph auth get-or-create client.glance | ssh root@controller01-{your-glance-api-server} sudo tee /etc/ceph/ceph.client.glance.keyring
osp9 # sudo chgrp glance /etc/ceph/ceph.client.glance.keyring
osp9 # sudo chmod 0640 /etc/ceph/ceph.client.glance.keyring

client.cinder   mon 'profile rbd' 
		osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images' 
		mgr 'profile rbd pool=volumes, profile rbd pool=vms'

client.cinder   mon 'allow r' 
		osd 'allow class-read object_prefix rbd_children, allow rwx pool=volumes, allow rx pool=images' 

client.cinder   mon 'allow r' 
		osd 'allow class-read object_prefix rbd_children, allow rwx pool=volumes, allow rwx pool=vms, allow rx pool=images'

client.cinder   mon 'allow r' 
		osd 'allow class-read object_prefix rbd_children, allow rwx pool=vms, allow rx pool=images'

client.cinder-backup    mon 'profile rbd' 
			osd 'profile rbd pool=backups' 
			mgr 'profile rbd pool=backups'

ceph-mon-01 $ sudo scp /etc/ceph/ceph.client.cinder.keyring root@controller01:/etc/ceph
ceph-mon-01 $ sudo ceph auth get-key client.cinder |ssh user@controller01  tee client.cinder.key
controller01 $ sudo chgrp cinder /etc/ceph/ceph.client.cinder.keyring
controller01 $ sudo chmod 0640 /etc/ceph/ceph.client.cinder.keyring

# ceph-mon-01  $ sudo scp /etc/ceph/ceph.client.cinder.keyring root@controller01:/etc/ceph/eph.client.nova.keyring 
# ceph-mon-01  $ sudo ceph auth get-key client.cinder |ssh {all-compute-node}  tee client.nova.key
# controller01  # sudo chgrp nova /etc/ceph/ceph.client.nova.keyring
# controller01  # sudo chmod 0640 /etc/ceph/ceph.client.nova.keyring

sudo ceph auth get-or-create client.cinder | ssh root@block01-{your-volume-server} sudo tee /etc/ceph/ceph.client.cinder.keyring
ssh block01-{your-cinder-volume-server} sudo chown cinder:cinder /etc/ceph/ceph.client.cinder.keyring
sudo ceph auth get-or-create client.cinder-backup | ssh root@block01-{your-cinder-backup-server} sudo tee /etc/ceph/ceph.client.cinder-backup.keyring
ssh root@block01-{your-cinder-backup-server} sudo chown cinder:cinder /etc/ceph/ceph.client.cinder-backup.keyring
sudo ceph auth get-or-create client.cinder | ssh root@controller01-{your-nova-compute-server} sudo tee /etc/ceph/ceph.client.cinder.keyring
sudo ceph auth get-key client.cinder | ssh root@computes-{your-compute-node} tee client.cinder.key

ceph $ sudo ceph auth get-or-create client.cinder | ssh root@controller tee /etc/ceph/ceph.client.cinder.keyring
ceph $ ssh root@controller chown cinder:cinder /etc/ceph/ceph.client.cinder.keyring
ceph $ scp /etc/ceph/ceph.conf root@pod0-spare:/etc/ceph/
ceph $ scp /etc/ceph/ceph.client.admin.keyring root@pod0-spare:/etc/ceph/
ceph $ ceph auth get-key client.cinder | ssh root@pod0-spare tee /etc/ceph/client.cinder.key

# ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
```

# Glance Integration
```sh
controller01/ceph-mon-01 $ sudo vim /etc/ceph/ceph.conf
[client.images]
keyring = /etc/ceph/ceph.client.images.keyring

controller01 $ sudo cp /etc/glance/glance-api.conf /etc/glance/glance-api.conf.orig

controller01 $ sudo vim /etc/glance/glance-api.conf
[glance_store]
stores = glance.ceph auth get-or-createstore.rbd.Store
default_store = rbd
rbd_store_pool = images
rbd_store_user = images
rbd_store_ceph_conf = /etc/ceph/ceph.conf

controller01 $ sudo systemctl restart glance-api.service

controller01 $ wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
controller01 $ qemu-img convert cirros-0.3.4-x86_64-disk.img cirros-0.3.4-x86_64-disk.raw
	       qemu-img convert cirros-0.4.0-x86_64-disk.img cirros-0.4.0-x86_64-disk.raw
controller01 $ glance image-create --name "Cirros 0.3.4" --disk-format raw --container-format bare --visibility public --file cirros-0.3.4-x86_64-disk.raw
	       glance image-create --name "cirros-ceph" --file cirros-0.4.0-x86_64-disk.raw --disk-format raw --container-format bare --visibility=public

ceph-mon-01 $ sudo rbd ls images

ceph-mon-01 $ sudo rbd info images/a55e9417-67af-43c5-a342-85d2c4c483f7
```

# Cinder Integration with Ceph
```sh
block01 $ sudo vim /etc/ceph/ceph.conf
[client.volumes]
#keyring = /etc/ceph/ceph.client.volumes.keyring
keyring = /etc/ceph/ceph.client.cinder.keyring

root@block01 # uuidgen |tee /etc/ceph/cinder.uuid.txt
controller01 $ sudo vim /etc/ceph/cinder.uuid.xml
ce6d1549-4d63-476b-afb6-88f0b196414f
client.volumes secret

cat > secret.xml <<EOF
<secret ephemeral='no' private='no'>
  <uuid>ce6d1549-4d63-476b-afb6-88f0b196414f</uuid>
  <usage type='ceph'>
    <name>client.cinder secret</name>
  </usage>
</secret>
EOF

block01 $ sudo virsh secret-define --file /etc/ceph/secret.xml

block01  # virsh secret-set-value --secret ce6d1549-4d63-476b-afb6-88f0b196414f --base64 $(cat /etc/ceph/client.cinder.key)
block01  $ sudo vi /etc/cinder/cinder.conf
[rbd]
volume_driver = cinder.volume.drivers.rbd.RBDDriver
rbd_pool = volumes
rbd_ceph_conf = /etc/ceph/ceph.conf
rbd_flatten_volume_from_snapshot = false
rbd_max_clone_depth = 5
rbd_store_chunk_size = 4
rados_connect_timeout = -1
glance_api_version = 2
rbd_user = volumes
rbd_secret_uuid = ce6d1549-4d63-476b-afb6-88f0b196414f

block01  $ openstack-service restart cinder

block01  $ sudo cinder create --display-name="test" 1

ceph-mon-01  $ sudo rbd ls volumes
volume-d251bb74-5c5c-4c40-a15b-2a4a17bbed8b

ceph-mon-01  $ sudo rbd info volumes/volume-d251bb74-5c5c-4c40-a15b-2a4a17bbed8b
```

# Nova Integration with Ceph
```sh
controller01  # sudo apt list installed python3-rbd ceph-common

controller01  # sudo vim /etc/ceph/ceph.conf
[client.nova]
keyring = /etc/ceph/ceph.client.nova.keyring

controller01  # sudo uuidgen |  tee /etc/ceph/nova.uuid.txt

controller01  # sudo vim /etc/ceph/secret.xml
c89c0a90-9648-49eb-b443-c97adb538f23
client.volumes secret

controller01  # sudo virsh secret-define --file /etc/ceph/nova.xml
controller01  # sudo virsh secret-set-value --secret c89c0a90-9648-49eb-b443-c97adb538f23 --base64 $(cat /etc/ceph/client.nova.key)
controller01  # sudo cp /etc/nova/nova.conf /etc/nova/nova.conf.orig

controller01  # sudo vi /etc/nova/nova.conf
force_raw_images = True
disk_cachemodes = writeback

[libvirt]
images_type = rbd
images_rbd_pool = vms
images_rbd_ceph_conf = /etc/ceph/ceph.conf
rbd_user = nova
rbd_secret_uuid = c89c0a90-9648-49eb-b443-c97adb538f23

controller01  # sudo systemctl restart openstack-nova-compute
controller01  # sudo neutron net-list
controller01  # sudo nova boot --flavor m1.small --nic net-id=4683d03d-30fc-4dd1-9b5f-eccd87340e70 --image='Cirros 0.3.4' cephvm
controller01  # sudo nova list

ceph-mon-01  $ sudo rbd -p vms ls
```

# Troubleshooting
```sh
controller01  ceph(keystone_admin)]# nova image-list
  
[root@controller01  ceph(keystone_admin)]# rbd -p images snap unprotect cf56345e-1454-4775-84f6-781912ce242b@snap
[root@controller01  ceph(keystone_admin)]# rbd -p images snap rm cf56345e-1454-4775-84f6-781912ce242b@snap
[root@controller01  ceph(keystone_admin)]# glance image-delete cf56345e-1454-4775-84f6-781912ce242b
```

Source:
https://superuser.openstack.org/articles/ceph-as-storage-for-openstack/


# Block Devices and OpenStack
```sh
# The nodes running glance-api, cinder-volume, nova-compute and cinder-backup act as Ceph clients. Each requires the ceph.conf file

ssh {your-openstack-server} sudo tee /etc/ceph/ceph.conf </etc/ceph/ceph.conf

sudo apt-get install python-rbd
sudo apt-get install ceph-common

compute-node
	uuidgen
	457eb676-33da-42ec-9a8c-9293d545c337

	cat > secret.xml <<EOF
	<secret ephemeral='no' private='no'>
	  <uuid>457eb676-33da-42ec-9a8c-9293d545c337</uuid>
	  <usage type='ceph'>
	    <name>client.cinder secret</name>
	  </usage>
	</secret>
	EOF
	sudo virsh secret-define --file secret.xml
	Secret 457eb676-33da-42ec-9a8c-9293d545c337 created
	sudo virsh secret-set-value --secret 457eb676-33da-42ec-9a8c-9293d545c337 --base64 $(cat client.cinder.key) && rm client.cinder.key secret.xml

sudo vim /etc/glance/glance-api.conf
	[glance_store]
	stores = rbd
	default_store = rbd
	rbd_store_pool = images
	rbd_store_user = glance
	rbd_store_ceph_conf = /etc/ceph/ceph.conf
	rbd_store_chunk_size = 8

	show_image_direct_url = True

/var/lib/glance/image-cache/
	flavor = keystone+cachemanagement

	[paste_deploy]
	flavor = keystone

	hw_scsi_model=virtio-scsi
	hw_disk_bus=scsi
	hw_qemu_guest_agent=yes
	os_require_quiesce=yes

/etc/cinder/cinder.conf
	[DEFAULT]
	...
	enabled_backends = ceph
	glance_api_version = 2
	...
	[ceph]
	volume_driver = cinder.volume.drivers.rbd.RBDDriver
	volume_backend_name = ceph
	rbd_pool = volumes
	rbd_ceph_conf = /etc/ceph/ceph.conf
	rbd_flatten_volume_from_snapshot = false
	rbd_max_clone_depth = 5
	rbd_store_chunk_size = 4
	rados_connect_timeout = -1

	[ceph]
	...
	rbd_user = cinder
	rbd_secret_uuid = 457eb676-33da-42ec-9a8c-9293d545c337

sudo vim /etc/cinder/cinder.conf
backup_driver = cinder.backup.drivers.ceph
backup_ceph_conf = /etc/ceph/ceph.conf
backup_ceph_user = cinder-backup
backup_ceph_chunk_size = 134217728
backup_ceph_pool = backups
backup_ceph_stripe_unit = 0
backup_ceph_stripe_count = 0
restore_discard_excess_bytes = true

[libvirt]
...
rbd_user = cinder
rbd_secret_uuid = 457eb676-33da-42ec-9a8c-9293d545c337

(Nova compute) node:
ceph daemon /var/run/ceph/ceph-client.cinder.19195.32310016.asok help

sudo vim /etc/ceph/ceph.conf 
[client]
rbd cache = true
rbd cache writethrough until flush = true
admin socket = /var/run/ceph/guests/$cluster-$type.$id.$pid.$cctid.asok
log file = /var/log/qemu/qemu-guest-$pid.log
rbd concurrent management ops = 20

mkdir -p /var/run/ceph/guests/ /var/log/qemu/
chown qemu:libvirtd /var/run/ceph/guests /var/log/qemu/

sudo glance-control api restart
sudo service nova-compute restart
sudo service cinder-volume restart
sudo service cinder-backup restart

cinder create --image-id {id of image} --display-name {name of volume} {size of volume}

qemu-img convert -f {source-format} -O {output-format} {source-filename} {output-filename}
qemu-img convert -f qcow2 -O raw precise-cloudimg.img precise-cloudimg.raw
```

Source:
https://docs.ceph.com/en/latest/rbd/rbd-openstack/

```sh
###############################################################################################################
ceph → libvrit → librbd → qemu

block $ install qemu, libvit ceph-client
block $ $ sudo apt -y install bridge-utils cpu-checker libvirt-clients libvirt-daemon qemu qemu-kvm ceph-common

controller $ mkdir -p /var/run/ceph/guests/ /var/log/qemu/
controller $ cat <<EOF>> /etc/ceph/ceph.conf
rbd default format = 2
admin socket = /var/run/ceph/\$cluster-\$type.\$id.\$pid.\$cctid.asok
log file = /var/log/qemu/qemu-guest-\$pid.log
rbd concurrent management ops = 20
[client.admin]
keyring = /etc/ceph/ceph.client.admin.keyring 
[client.cinder]
keyring = /etc/ceph/ceph.client.cinder.keyring
[client.glance]
keyring = /etc/ceph/ceph.client.glance.keyring
EOF

controller $ uuidgen > /root/uuid

controller $ cat > /etc/ceph/secret.xml <<EOF
<secret ephemeral="no" private="no">
<uuid>`cat /root/uuid`</uuid>
<usage type="ceph">
<name>client.cinder secret</name>
</usage>
</secret>
EOF

virsh secret-define --file /etc/ceph/secret.xml
virsh secret-set-value --secret `cat /root/uuid` --base64 $(cat /etc/ceph/client.cinder.key) && rm /etc/ceph/client.cinder.key /etc/ceph/secret.xml

openstack-config --set /etc/cinder/cinder.conf DEFAULT enabled_backends ceph

block01 $ sudo vim  /etc/cinder/cinder.conf
[lvm]

[ceph]
volume_driver = cinder.volume.drivers.rbd.RBDDriver
rbd_cluster_name = ceph
rbd_pool = volumes
rbd_user = cinder
rbd_ceph_conf = /etc/ceph/ceph.conf
rbd_flatten_volume_from_snapshot = false
rbd_secret_uuid = 4b5fd580-360c-4f8c-abb5-c83bb9a3f964
rbd_max_clone_depth = 5
rbd_store_chunk_size = 4
rados_connect_timeout = -1

backup_driver = cinder.backup.drivers.ceph
backup_ceph_user = cinder-backup
backup_ceph_conf = /etc/ceph/ceph.conf
backup_ceph_chunk_size = 134217728
backup_ceph_pool = backups
backup_ceph_stripe_unit = 0
backup_ceph_stripe_count = 0
restore_discard_excess_bytes = true
systemctl restart openstack-cinder-api.service
systemctl restart openstack-cinder-volume.service
systemctl restart openstack-cinder-scheduler.service


controller $ cat  /etc/openstack-dashboard/local_settings | grep enable_backup
OPENSTACK_CINDER_FEATURES = {
    'enable_backup': True,
}


source ~/keystonerc_admin

cinder type-create ceph
cinder type-key ceph set volume_backend_name=ceph
cinder service-list
cinder create --volume-type ceph --display-name test 1

openstack volume list

rbd -p volumes ls
rbd -p volumes ls > volume-id
rbd -p volumes info `cat volume-id`

openstack volume delete test
openstack volume list
cat volume-id
```

Sources:
https://access.redhat.com/documentation/en-us/red_hat_ceph_storage/2/html/ceph_block_device_to_openstack_guide/configuring_openstack_to_use_ceph
http://onecloudclass.com/lab-12-integrate-ceph-with-cinder/

