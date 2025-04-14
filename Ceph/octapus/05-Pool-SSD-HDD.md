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
rbd pool init ssd_pool

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

6. Create Volume

```sh
rbd create --size 10G --pool ssd_pool ssd_volume
rbd create --size 10G --pool hdd_pool hdd_volume
rbd ls --pool ssd_pool -l
rbd ls --pool hdd_pool -l
```

7. CephX client 
- On ceph cluster
```sh
ceph auth ls
ceph auth add client.hdd mon 'allow r' osd 'allow rwx pool=hdd_pool'
ceph auth get client.hdd


ceph auth ls
ceph auth add client.ssd mon 'allow r' osd 'allow rwx pool=ssd_pool'
ceph auth get client.ssd
# COPUY AUTH
ceph config generate-minimal-conf     # cat /etc/ceph/ceph.config
# COPY CONFIG
```

- On clients
```sh
sudo vim /etc/ceph/ceph.conf
# PASTE CONFIG

sudo vim /etc/ceph/ceph.keyring
# PASTE AUTH
```

8. Mount and mapp on client

```sh
rbd -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.keyring -n client.hdd ls pool --pool hdd_pool -l
sudo rbd -n client.hdd device map --pool hdd_pool  hdd_volume
sudo mkfs.ext4 /dev/rbd0
fdisk -l
sudo mount /dev/rbd0 /mnt 
df -h
sudo umount /dev/rdb0
sudo rbd unmap /dev/rbd0

rbd -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.keyring -n client.ssd ls pool --pool ssd_pool -l
sudo rbd -n client.ssd device map --pool ssd_pool ssd_volume
sudo mkfs.ext4 /dev/rbd1
fdisk -l
sudo mount /dev/rbd1 /mnt 
df -h
sudo umount /dev/rdb1
sudo rbd unmap /dev/rbd1
```
