
Introduction
Ceph is a powerful open-source storage platform that provides unified storage for block, object, and file workloads. One of its key features is the RADOS Block Device (RBD), which offers block storage similar to AWS EBS volumes.

In this tutorial, we'll demonstrate how to use a Ceph RBD volume as persistent storage for MariaDB on an Ubuntu 22.04 server. This setup is especially useful for high-availability and distributed environments where multiple clients may need access to the same data.

We will cover the entire process—from creating the Ceph pool and volume to mounting the volume on a client machine and configuring MariaDB to use it as its data directory. By the end, you’ll also see how to access the same database volume from another host using the Ceph cluster.

💡 All commands and configuration files used in this tutorial are available on my GitHub repository.

Step 1: Create a Ceph Block Storage Pool
Before we can create a block device (RBD), we need a storage pool in the Ceph cluster. A pool is a logical group of storage objects, and it's where our RBD volume will reside.

Let’s create a pool named mariadb-pool and initialize it for RBD usage:

![scenario](https://github.com/hojat-gazestani/openstack/blob/main/Ceph/octapus/PICs/ceph-mariadb.png)

```sh
ceph osd pool create mariadb-pool 
ceph osd pool ls detail         
rbd pool init mariadb-pool         
ceph osd pool ls detail | grep application 
```

Step 2: Create an RBD Volume
Now that we have a storage pool, we can create an RBD image (volume) inside it. This volume will act like a raw disk that we can attach and mount on our Linux client.

Let’s create a 10 GB RBD volume named mariadb-volume:

```sh
rbd create --size 10G --pool mariadb-pool mariadb-volume  
rbd ls --pool mariadb-pool -l  
rbd ls -l
rbd info mariadb-pool
rbd info mariadb-pool/mariadb-volume
```

Step 3: Configure CephX Authentication
Ceph uses a built-in authentication system called CephX to secure access to its services. Since we’re working with a shared storage cluster, it’s important to create a restricted client that only has access to the resources it needs.

Let’s create a client named client.mariadb with:

Read access to the monitor (mon)

Read/write/execute access to the mariadb-pool


```sh
ceph auth add client.mariadb mon 'allow r' osd 'allow rwx pool=mariadb-pool'  
ceph auth get client.mariadb  
```

Next, generate a minimal Ceph config to be used on the client machine:

```sh
# Ceph cluster configuration to login
ceph config generate-minimal-conf
```

# Step4:Preparing Cleint machine 

Install Ceph tools.

```sh
CEPH_RELEASE=19.2.1
curl --silent --remote-name --location https://download.ceph.com/rpm-${CEPH_RELEASE}/el9/noarch/cephadm
chmod +x cephadm
sudo ./cephadm add-repo --release squid
sudo apt update -y
sudo apt install ceph-common -y
ceph -v
```

Add ceph config and keyring
```sh
sudo vim /etc/ceph/ceph.conf  
# Paste minimal Ceph config

sudo vim /etc/ceph/ceph.keyring  
# Paste client.mariadb’s keyring
```

Load the RBD kernel module:

```sh
sudo modprobe rbd
```

# Step 5: Mapping and Mounting RBD volume on the client

Attach the RBD volume to our linux machine and mount it. 

```sh
rbd -n client.mariadb device map --pool mariadb-pool mariadb-volume  
sudo mkfs.ext4 /dev/rbd0 
mkdir /var/lib/mysql 
sudo mount /dev/rbd0 /var/lib/mysql  
ls -l /var/lib/mysql
df -h | grep rbd  
```

# Step 6: Install MariaDB and use Ceph storage backend
# MariaBD
```sh
apt install -y mariadb-server
systemctl start mariadb
systemctl enable mariadb
systemctl status mariadb

mysql -u root
create database cephrbd
show databases;

systemctl stop mariadb
umount /var/lib/mysql
```

# Step 7: Install MariaDB on another second client and use the databases

if we mount the ceph volume we can see all data are available on the new host through the ceph cluster

```sh
rbd -n client.mariadb device map --pool mariadb-pool mariadb-volume  
sudo mkfs.ext4 /dev/rbd0 
mkdir /var/lib/mysql 
sudo mount /dev/rbd0 /var/lib/mysql  
ls -l /var/lib/mysql
df -h | grep rbd  

````

```sh
apt install -y mariadb-server
systemctl start mariadb
systemctl enable mariadb
systemctl status mariadb

mysql -u root
show databases;

systemctl stop mariadb
umount /var/lib/mysql
```
