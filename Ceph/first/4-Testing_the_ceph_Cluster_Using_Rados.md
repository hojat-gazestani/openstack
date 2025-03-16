# Perform the pre-installation Steps on the Client-node

```sh
ceph@admin-node$ /Working-Directory/ ceph-deploy install -rgw <gateway-node>
ceph@admin-node$ ceph-deploy rgw create 					# Create an instance of the Ceph Object gateway
ceph@admin-node$ sudo systemctl status ceph-radosgw.service # Make sure is running
ceph@		   $ curl http://<client-node>/7480				# You should now be able to make an unauthenticated request to the gateway on its default port
```

# Writing benchmarks
```sh
rados -p mypool bench <seconds> write|seq|rand [-t concurrent_operations] [--no-cleanup]
--no-cleanup flag will leave data generated during the write test on your pool, which is required for the read test.

rados -p mypool bench 60 write --no-cleanup

# Reading Benchmarks
rados -p mypool bench 60 rand

# Disk Latency Benchmarks
rados -p mypool bench 60 write --no-cleanup -t 500

# Read latency checking
rados -p mypool bench 60 rand -t 500
```