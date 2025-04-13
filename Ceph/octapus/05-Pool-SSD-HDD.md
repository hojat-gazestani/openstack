# Create Pools for SSD and HDD

## Steps to Create Pools for SSD and HDD

1. Verify OSD Classes

```sh
ceph osd tree
ceph osd crush class ls
```

2. Create CRUSH Rules for SSD and HDD


```sh
ceph osd crush rule list
ceph osd crush rule dump

# `host` replicas are placed on different hosts for fault tolerance
ceph osd crush rule create-replicated {rule-name} {CRUSH-hierarchy} host {device-classes}

# Create a CRUSH rule for HDD
ceph osd crush rule create-replicated hdd_rule default host hdd

# Create a CRUSH rule for SSD
ceph osd crush rule create-replicated ssd_rule default host ssd

ceph osd crush rule list
ceph osd crush rule dump

```


3. Create Pools with the Rules

```sh
# `replicated` specifies that the pool uses replication (not erasure coding).
ceph osd pool create {pool-name} {pg} {pgp} replicated {CRUSH-rules}

# Create a pool for HDD
ceph osd pool create hdd_pool 128 128 replicated hdd_rule

# Create a pool for SSD
ceph osd pool create ssd_pool 128 128 replicated ssd_rule

```

4. Verify the Pools

```sh
ceph osd pool ls detail
```

5. Enable Application Tags
```sh
# Sets up internal RBD metadata in the pool
rbd pool init hdd_pool
rbd pool init ssh_pool

# list any RBD images, which confirms the pool is functional and metadata is in place.
rados -p hdd_pool ls
# inspect RBD stores metadata in omap key/value pairs.
rados -p hdd_pool listomapkeys rbd_directory
#  inspect the key
rados -p hdd_pool getomapval rbd_directory rbd_id.myimage -

# Registers the pools as being used by the RBD application
ceph osd pool application enable hdd_pool rbd
ceph osd pool application enable ssd_pool rbd

```

## Using the Pools

```sh
CEPH_RELEASE=19.2.1
curl --silent --remote-name --location https://download.ceph.com/rpm-${CEPH_RELEASE}/el9/noarch/cephadm
chmod +x cephadm
sudo ./cephadm add-repo --release squid
sudo apt update -y
sudo apt install ceph-common -y
ceph -v
sudo vim /etc/ceph/ceph.conf
# PASTE CONFIG

sudo vim /etc/ceph/ceph.keyring
# PASTE AUTH
```

```sh
lsmod | grep rbd
modprobe rbd

rbd -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.keyring -n client.test ls pool --pool test-pool -l 
sudo rbd -n client.test device map --pool test-pool test-volume
# /dev/rbd0

sudo mkfs.ext4 /dev/rbd0
fdisk -l
sudo mount /dev/rbd0 /mnt 
df -h
sudo umount /dev/rdb0
sudo rbd unmap /dev/rbd0
```
