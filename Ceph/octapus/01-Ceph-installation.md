# ceph installation


- on all nodes
```sh
CEPH_RELEASE=18.2.0
CEPH_RELEASE=17.2.6

curl --silent --remote-name --location https://download.ceph.com/rpm-${CEPH_RELEASE}/el9/noarch/cephadm

chmod +x cephadm

./cephadm add-repo --release quincy
/cephadm install

apt update
apt policy cephadm
apt install cephadm
```

## Bootstrap a new cluster

```sh
cephadm bootstrap --mon-ip *<mon-ip>*
./cephadm bootstrap --mon-ip 192.168.1.1 --initial-dashboard-user admin --initial-dashboard-password 123456

cephadm shell
ceph --version
ceph -s
ceph -w
ceph df
```

## adding host

- on the first noe
```sh
cat /etc/ceph/ceph.pub
COPY PUB KEY
```
- on the other nodes
```sh
vim /root/.ssh/authorizekey
PASTE KEY HERE
```

- Add host
```sh


ceph orch host add ceph02 192.168.1.2
ceph orch host ls
ceph orch host add ceph03 192.168.1.3
ceog orch host ls

ceph orch host label add ceph02 _admin
ceph orch host label add ceph03 _admin
ceph -s
ceph orch ps
```

## Adding Storage

```sh
ceph orch ls

ceph orch apply osd --all-available-devices --dry-run
ceph orch apply osd --all-available-devices
ceph orch ls
ceph orch ps
ceph -s		# health OK
```

```txt
OSD status:
	up
	in
	out
	down
```

```sh
ceph osd tree
# look at osd distribution

ceph pg ls
ceph osd pool ls
ceph osd pool ls detail
```

## placement group

```txt
pool: Logical volume, placement group

Note: each PG can assign to one pool
pool1: PG1, PG2, PG3, PG4
pool2: PG5, PG6, PG7, PG9

Placement group map:
	specify which object location for specific user - scailable

pool -> pg :
			pg_num 		32, 64, 128
			pgp_num		auto scailing

Search: setting the number of pgs ceph

```

## Pool, volume

- Creating pool
```sh
ceph -s

ceph osd pool create bdpooltest 64 # 64 placement group
ceph osd pool ls detail
# replication size 3
# pg_num 64
# pgp_num 64
# autoscalig_mode on

# initial pool as block device
rbd pool init bdpooltest
ceph osd pool ls detail
# application rbd
```

- Creating volume
```sh
# create volume
rbd create --size 10G --pool bdpooltest bdvolumetest
rbd ls --pool bdpooltest -l
rbd --pool bdpooltest rm bdvolumetest

```

- Creating user
```sh
ceph auth ls
ceph auth add client.test mon 'allow r' osd 'allow rwx pool=bdpooltest'
ceph auth get client.test
```

## Ceph client

- Create a linux a ceph client
- Add updated repository
```sh
apt update
apt search ceph-common

#search ceph add repository
CEPH_RELEASE=18.2.0
CEPH_RELEASE=17.2.6

curl --silent --remote-name --location https://download.ceph.com/rpm-${CEPH_RELEASE}/el9/noarch/cephadm

chmod +x cephadm

./cephadm add-repo --release quincy
apt search ceph-common
apt install ceph-common
ceph -v
ls /etc/ceph/
rbdmap
```

- On the server
```sh
cephadm shell
cat /etc/ceph/ceph.conf
ceph config generate-minimal-conf
# COPY OUTPUT
```

- On ther client
```sh
vim /etc/ceph/ceph.conf
# PASTE here
```

- On the server
```sh
ceph auth get client.test
# COPY OUTPUT
````

- On ther client
```sh
vim /etc/ceph/ceph.keyring # defualt /etc/ceph/ceph.keyring
# PAST here
```

- On the client
```sh
lsmod | grep rbd
modprobe rbd
lsmod | grep rbd

rbd ls -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.keyring -n client.test --pool bdpooltest

rbd ls -n client.test --pool bdpooltest
```

- Map the volume on OS to recogonize as a device
```sh
rbd --help | grep map

rbd -n client.test device map --pool bdpooltest bdvolumetest
file /dev/rbd0

mkfs.ext4 /dev/rbd0
fdisk -l
mount /dev/rbd0 /mnt
df -h
cd /mnt
ls
dd if=/dev/random of=/.bigfile bs=100M count=10
```

- On server
```bash
ceph -s
ceph device ls
```

## Permanent Mount Block device
- search: how to boot ceph rbd
- on server
```sh
rbd  ls --pool bdpooltest -l
```

- on client
```sh
rbd -n client.test ls --pool bdpooltest -l
rbd -n client.test mapp --pool bdpooltest bdvolumetest
df -h
mount /dev/rbd0 /opt	# it is not permanent
```

```sh
systemctl status rbdmap.service
systemctl cat rbdmap.service

cat /etc/ceph/rbdmap
vim /etc/ceph/rbdmap
bdpooltest/bdvolumetest id=test,keyring=/etc/ceph/ceph.keyring

systemctl status rbdmap.service
systemctl restart rbdmap.service
ls /dev/rbd

vim /etc/fstab
/dev/rbd/bdpooltest/bdvolumetest	/opt 	ext4 	noauto 0 0
```

## CRUSH MAP, Placement group

- manually editing crush map
```sh
ceph osd getcrushmap -o crush.e
crushtool -d crush.e -o crush.d
vim crush.d
crushtool -c crush.d -o crush.new.o
ceph osd setcrushmap  crush.new.o
```

## Object storage

```sh
Block storage
cdphfs - nfs
Object storage
	API
	Bucket

PIC-1
```
- On server
```sh
ceph -s
ceph orch ls
ceph orch apply rgw tgwtest
ceph orch ps
ceph osd pool ls

radosgw-admin user create --uid=johndoe --display-name="John Doe" --email=john@example.com
radosgw-admin user help
radosgw-admin user list
radosgw-admin user info --uid johndoe
# COPY access key, secret key
```

- On client
```sh
aws configure --profile=johndoe
access key:user key
secrect key: secret key
output format: json


cat ~/.aws/config
cat ~/.aws/credentials


aws --profile johndoe --endpoint-url https://192.168.1.2 s3 mb s3://bucket0

```

- On server
```sh
radosgw-admin bucket list
# see you bucket
radosgw-admin bucket stats
```

- On client
```sh
aws --profile johndoe --endpoint-url https://192.168.1.2 put-object --bucket bucket0 --key testfile --body /etc/services

aws --profile johndoe --endpoint-url https://192.168.1.2 list-objects

```

## Select Pool for Object storage

```sh
ceph -s

ceph health detail
ceph osd pool ls

ceph orch ps
ceph orch rm rgw.tg

```
