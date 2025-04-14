# SSDs as a cache layer for HDDs

- The SSD pool acts as a cache tier for frequently accessed ("hot") data
- The HDD pool acts as the base tier for storing all data, including less frequently accessed ("cold") data.

- Ceph automatically promotes hot data to the cache tier (SSD) and demotes cold data to the base tier (HDD).

## Create CRUSH Rules for SSD and HDD
```sh
ceph osd crush class ls
ceph osd crush rule list
ceph osd crush rule dump

ceph osd crush rule create-replicated hdd_rule default host hdd
ceph osd crush rule create-replicated ssd_rule default host ssd
```

## Steps to Set Up SSD as a Cache Tier for HDD

1. Create the Base Tier (HDD Pool)

```sh
ceph osd pool create hdd_pool 128 128 crush_rule=hdd_rule
```

2. Create the Cache Tier (SSD Pool)
```sh
ceph osd pool create ssd_cache_pool 128 128 crush_rule=ssd_rule
```
- Verification
```sh
ceph osd pool get hdd_pool crush_rule
ceph osd pool get ssd_cache_pool crush_rule
```
3. Set Up Cache Tiering
```sh
ceph osd tier add hdd_pool ssd_cache_pool
```

4. Configure Cache Mode
```sh
ceph osd tier cache-mode ssd_cache_pool writeback
```

- writeback mode:

```txt
Data is written to the cache tier (SSD) first and then flushed to the base tier (HDD) later.

Reads are served from the cache tier if the data is present; otherwise, data is read from the base tier and promoted to the cache tier.
```

5. Set Cache Tiering Parameters

```sh
# Set the maximum size of the cache tier.
ceph osd pool set ssd_cache_pool target_max_bytes 100000000000  # 100GB

# Set the maximum number of objects in the cache tier.
ceph osd pool set ssd_cache_pool target_max_objects 1000000  # 1 million objects

# Define how many hit sets to track for promoting data.
ceph osd pool set ssd_cache_pool hit_set_count 8

# Define the time period for tracking hits.
ceph osd pool set ssd_cache_pool hit_set_period 300  # 300 seconds

# Minimum number of hits required to promote data.
ceph osd pool set ssd_cache_pool min_read_recency_for_promote 2

# Minimum number of hits required to promote data.
ceph osd pool set ssd_cache_pool min_write_recency_for_promote 2

# object-based cache limit
ceph osd pool set ssd_cache_pool target_max_objects 1000000  # Adjust based on expected object size

# cache eviction thresholds
ceph osd pool set ssd_cache_pool cache_target_dirty_ratio 0.4
ceph osd pool set ssd_cache_pool cache_target_full_ratio 0.8

ceph osd pool set ssd_cache_pool hit_set_type bloom
ceph osd pool set ssd_cache_pool hit_set_fpp 0.05  # 5% false positive rate

# writeback safety
ceph osd pool set ssd_cache_pool cache_min_flush_age 600  # 10 minutes
ceph osd pool set ssd_cache_pool cache_min_evict_age 1800  # 30 minutes

# Performance monitoring
ceph osd pool set ssd_cache_pool target_max_bytes 100000000000  # 100GB

```

6. Enable Overlay
```sh
ceph osd tier set-overlay hdd_pool ssd_cache_pool
```

7. Verify the Setup
```sh
ceph osd dump | grep tier
```

## Example Configuration

- Base Tier (HDD Pool):
```sh
ceph osd pool create hdd_pool 128 128
ceph osd pool application enable hdd_pool rbd
```

- Cache Tier (SSD Pool):
```sh
ceph osd pool create ssd_cache_pool 128 128
ceph osd pool application enable ssd_cache_pool rbd
```

- Tiering Setup:
```sh
ceph osd tier add hdd_pool ssd_cache_pool
ceph osd tier cache-mode ssd_cache_pool writeback
ceph osd pool set ssd_cache_pool target_max_bytes 100000000000  # 100GB
ceph osd pool set ssd_cache_pool hit_set_count 8
ceph osd pool set ssd_cache_pool hit_set_period 300
ceph osd pool set ssd_cache_pool min_read_recency_for_promote 2
ceph osd pool set ssd_cache_pool min_write_recency_for_promote 2
ceph osd tier set-overlay hdd_pool ssd_cache_pool
ceph osd pool set ssd_cache_pool target_max_objects 1000000  # Adjust based on expected object size
ceph osd pool set ssd_cache_pool cache_target_dirty_ratio 0.4
ceph osd pool set ssd_cache_pool cache_target_full_ratio 0.8
ceph osd pool set ssd_cache_pool hit_set_type bloom
ceph osd pool set ssd_cache_pool hit_set_fpp 0.05  # 5% false positive rate
ceph osd pool set ssd_cache_pool cache_min_flush_age 600  # 10 minutes
ceph osd pool set ssd_cache_pool cache_min_evict_age 1800  # 30 minutes
ceph osd pool set ssd_cache_pool target_max_bytes 100000000000  # 100GB
```

## Monitoring and Managing Cache Tiering

1. Check Cache Tier Status:
```sh
ceph df
```

2. Flush Cache:
```sh
rados -p ssd_cache_pool cache-flush-evict-all
```

- Adjust Cache Parameters:

```txt
adjust cache parameters (e.g., target_max_bytes, hit_set_count) based on your workload and performance requirements.
```

3. Disable Cache Tiering:

```sh
ceph osd tier remove-overlay hdd_pool
ceph osd tier remove hdd_pool ssd_cache_pool
```

## Advantages of Cache Tiering


- **Improved Performance**: Frequently accessed data is served from the faster SSD tier.

- **Cost Efficiency**: Less frequently accessed data is stored on the cheaper HDD tier.

- **Automatic Data Management**: Ceph automatically promotes and demotes data based on access patterns.


## Considerations

1. Writeback Mode Risks:
    - In writeback mode, data is written to the cache tier first. If the cache tier fails before data is flushed to the base tier, data loss can occur.
    - Ensure proper monitoring and redundancy for the cache tier.

2. Cache Sizing:
    - Size the cache tier appropriately to balance performance and cost. Too small a cache may not provide significant performance benefits; too large a cache may be unnecessarily expensive.

3. Workload Suitability:
    - Cache tiering works best for workloads with a high degree of locality (e.g., frequently accessed data). For random or write-heavy workloads, the benefits may be limited.

## Init the pool
```sh
rbd pool init ssd_cache_pool
ceph osd pool application enable ssd_cache_pool rbd
```

## Create volume
```sh
rbd create --size 10G --pool ssd_cache_pool ssd_cache_volume
rbd ls --pool ssd_cache_pool -l
```

## CephX client
```
ceph auth add client.cache mon 'allow r' osd 'allow rwx pool=ssd_cache_pool'
ceph auth get client.cache
# COPUY AUTH
ceph config generate-minimal-conf     # cat /etc/ceph/ceph.config
# COPY CONFIG
```

## Client config
```sh
sudo vim /etc/ceph/ceph.conf
# PASTE CONFIG

sudo vim /etc/ceph/ceph.keyring
# PASTE AUTH
```

## Mount and mapp on client
```sh
rbd -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.keyring -n client.cache ls pool --pool ssh_cache_pool -l
sudo rbd -n client.cache device map --pool ssh_cache_pool  ssd_cache_volume
sudo mkfs.ext4 /dev/rbd0
fdisk -l
sudo mount /dev/rbd0 /mnt 
df -h
sudo umount /dev/rdb0
sudo rbd unmap /dev/rbd0
```
