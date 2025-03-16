# Installing the client
```sh
#  Ceph FS is not as stable as the rdb and the Ceph gateway
ceph@admin-node$ ceph-deploy install ceph-client	# Deploy the client
ceph@admin-node$ ceph -s		# ensure that the storage cluster is running and is clean state
```

# Creating a File system

```sh
ceph@admin-node$ ceph osd pool create cephfs_data <pg_num>	# Create some pools 
ceph@admin-node$ ceph osd pool create cephfs_metadata <pg_num>
ceph@admin-node$ ceph fs new <fs_name> dephfs_metadata cephfs_data
```

# Create a Secret file
```sh
# The Ceph Storage cluster runs with authentication turned on by default. To authenticate, the client needs a secret key file.
$ cat ceph.client.admin.keyring	# Find a key for a user within a keyring file
# Copy the key of the user that will be using the mounted Ceph FS File system
	[client.admin]
	key = AVILHEBW/9856...
# Copy the key from the previous file and paste it into an empty file that has the user name in its name (e.g admin.secret). This file contains just the key
# Set the file permission such that key is not visible to other users
$ sudo mkdir /mnt/mycephfs
$ sudo mount -t ceph {monitor-ip}:6789://mnt/mycephfs - o name=admin,secretfile=admin.secret
```