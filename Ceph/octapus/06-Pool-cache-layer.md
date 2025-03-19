# SSDs as a cache layer for HDDs

- The SSD pool acts as a cache tier for frequently accessed ("hot") data
- The HDD pool acts as the base tier for storing all data, including less frequently accessed ("cold") data.

- Ceph automatically promotes hot data to the cache tier (SSD) and demotes cold data to the base tier (HDD).

## Steps to Set Up SSD as a Cache Tier for HDD

1. Create the Base Tier (HDD Pool)

```sh
ceph osd pool create hdd_pool 128 128
```

2. Create the Cache Tier (SSD Pool)
```sh
ceph osd pool create ssd_cache_pool 128 128
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
