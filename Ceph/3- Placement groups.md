# PLACEMENT GROUPS

+ PG: How Ceph distribute data.

+ Autoscaling: Cluster make recommendations.
+ Manually adjust pg_num: for each pool based on expected cluster and pool utilization.

## pg_autoscale_mode
```txt
off : Disable autoscaling.
on  : Enable autoscaling (PG count)
warn: Raise health alerts.
```

## Set autoscaling mode
```sh
ceph osd pool set <pool_name> pg_autoscale_mode  <mode>
```

### Configure the defualt pg_autoscale_mode
```sh
ceph config set global osd_pool_default_pg_autoscale_mode <mode>
```

## noautoscale for all pool
