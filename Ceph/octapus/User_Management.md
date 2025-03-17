```txt
ceph health = ceph -n client.admin --keyring=/etc/ceph/ceph.client.admin.keyring health

Pool: The type of Ceph clien (e.g., Block Device, Object Storage, Filesystem, native API, etc.),Ceph stores all data as objects within pools.

Type of access:
Read:
Write
xecute: Ceph’s administrative commands
```

# User

```txt
individual or a system actor 
Who or What  can access your Ceph Storage Cluster, its pools, and the data within pools.

TYPE.ID
client.admin
client.user1

capabilities:  authorizing an authenticated user to exercise the functionality of the monitors, OSDs and metadata servers
				capabilities can also restrict access to data within a pool, a namespace within a pool, or a set of pools based on their application tags.
				
	{daemon-type} '{cap-spec}[, {cap-spec} ...]'
	
	
	mon 'allow {access-spec} [network {network/prefix}]'
		e.g.
			{access-spec}
				* | all | [r][w][x]
			{network/prefix}
				10.3.0.0/16

	mon 'profile {name}'	
		* | all | [r][w][x] 
```

# OSD Caps
```txt
	osd 'allow {access-spec} [{match-spec}] [network {network/prefix}]'
		e.g.
			{access-spec}
				* | all | [r][w][x] [class-read] [class-write]
				class {class name} [{method name}]
			{match-spec}
				pool={pool-name} [namespace={namespace-name}] [object_prefix {prefix}]	
				[namespace={namespace-name}] tag {application} {key}={value}
			{network/prefix}
				10.3.0.0/16

	osd 'profile {name} [pool={pool-name} [namespace={namespace-name}]] [network {network/prefix}]'
```

# Manager Caps
```txt
	mgr 'allow {access-spec} [network {network/prefix}]'
		e.g.
			 {access-spec}
			 	* | all | [r][w][x]
	mgr 'profile {name} [{key1} {match-type} {value1} ...] [network {network/prefix}]'
		e.g.
			{match-type}
				= | prefix | regex


	mgr 'allow command "{command-prefix}" [with {key1} {match-type} {value1} ...] [network {network/prefix}]'
	mgr 'allow service {service-name} {access-spec} [network {network/prefix}]'
		e.g.
			{service-name}
				mgr | osd | pg | py

	mgr 'allow module {module-name} [with {key1} {match-type} {value1} ...] {access-spec} [network {network/prefix}]'
```

# Metadata Server Caps:

	

# Managing Users

```sh
ceph auth ls
ceph auth get {TYPE.ID} : ceph auth get client.admin
ceph auth export {TYPE.ID
```

## Add a User
```sh
ceph auth add client.john mon 'allow r' osd 'allow rw pool=liverpool'
ceph auth get-or-create client.paul mon 'allow r' osd 'allow rw pool=liverpool'
ceph auth get-or-create client.george mon 'allow r' osd 'allow rw pool=liverpool' -o george.keyring
ceph auth get-or-create-key client.ringo mon 'allow r' osd 'allow rw pool=liverpool' -o ringo.key
```

## Modify User Capabilities

```sh
ceph auth get client.john
ceph auth caps client.john mon 'allow r' osd 'allow rw pool=liverpool'
ceph auth caps client.paul mon 'allow rw' osd 'allow rwx pool=liverpool'
ceph auth caps client.brian-manager mon 'allow *' osd 'allow *'
```

## Delete a User

```sh
ceph auth del {TYPE}.{ID}

ceph auth print-key {TYPE}.{ID}	
```

Sources:

https://docs.ceph.com/en/latest/rados/operations/user-management/
				
