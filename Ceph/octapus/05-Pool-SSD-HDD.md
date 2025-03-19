# Create Pools for SSD and HDD

## Steps to Create Pools for SSD and HDD

1. Verify OSD Classes

```sh
ceph osd tree
ceph osd crush class ls
```

2. Create CRUSH Rules for SSD and HDD


```sh
ceph osd crush rule create-replicated {rule-name} {CRUSH-hierarchy} host {device-classes}
# `host` replicas are placed on different hosts for fault tolerance

# Create a CRUSH rule for HDD
ceph osd crush rule create-replicated hdd_rule default host hdd

# Create a CRUSH rule for SSD
ceph osd crush rule create-replicated ssd_rule default host ssd
```


3. Create Pools with the Rules

```sh
ceph osd pool create {pool-name} {pg} {pgp} replicated {CRUSH-rules}
# `replicated` specifies that the pool uses replication (not erasure coding).

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
ceph osd pool application enable hdd_pool rbd
ceph osd pool application enable ssd_pool rbd
```

##  Example Output After Setup
```sh
ceph osd crush rule ls

ceph osd pool ls detail
```

## Using the Pools

```sh
# For RBD (Block Storage)
rbd create hdd_pool/myimage --size 10G
rbd create ssd_pool/myimage --size 10G

# For CephFS
ceph fs new myfs ssd_pool hdd_pool
```