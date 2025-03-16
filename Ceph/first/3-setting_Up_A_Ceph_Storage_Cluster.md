# Working with the Ceph Cluster

```sh
$ ceph osd lspools 				# Check current pools
$ ceph osd pool creat test 50 	# Create a pool and verify it, using 50 placement groups
$ echo Hello >> /tmp/test.txt	# Create an object to store
$ rados put try-1 /tmp/test.txt --pool test	# Add the object to the store
$ rados -p test ls try-1		# Verify success
$ rados get try-1 /tmp/somefile --pool=test	# Get the file
```

# Create Ceph pool
```sh
ceph osd pool create {pool-name} {pg-num} [{pgp-num}] [replicated] [crush-ruleset-name]
ceph osd pool create mypool 2000 2000 pool 'mypool' created
```

# Installing Ceph on the Client
```sh
# You'll need a ceph client to run the RADOS Block Device (RBD)
ceph@admin-node$ ceph-deploy install ceph-client	# Make sure that the admin node is set up to reach the client using host names.
$ ceph-deploy admin ceph-client		# Copy the required configuration files to the client
```

# Configuring the Block Device
```sh
ceph@client-nodes$ rdb create foo --size 4096				# Create block device
ceph@			 $ sudo rbd map foo --name client.admin		# To map the image to the block device
ceph@			 $ sudo mkfs.ext4 -m0 /dev/rdb/rbd/foo		# Create file system, use it like any other block device
```