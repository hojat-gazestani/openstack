# Setting up Ceph Prerequisites on Centos
```sh
# On the ceph admin node:
ceph@admin-node$ sudo yum -y update; reboot
ceph@admin-node$ vim /etc/yum.repos.d/start-ceph.repo
	[ceph-noarch]
	name=Ceph noarch Packages
	baseurl=http://ceph.com/rpm-hammer/el7/noarch
	enabled=1
	gpgcheck=1
	type=rpm-md
	gpgkey=https://ceph.com/git/?p=ceph.git;a-blob_plain;f=keys/release.asc

for i in {1..3}; do scp /etc/yum.repos.d/start-ceph.repo cephs$i:/etc/yum.repos.d/; done

ceph@admin-node$ timedatectl													

ceph@admin-node$ sudo useradd -d /home/ceph -m ceph
ceph@admin-node$ echo 'ceph:openstack' | sudo chpasswd
# OR
ceph@admin-node$ useradd ceph; echo openstack | passwd --stdin ceph				

ceph@admin-node$ echo "ceph ALL = (root) NOPASSWD: ALL" > /etc/sudoers.d/ceph	
ceph@admin-node$ chmod 0400 /etc/sudoers.d/ceph
ceph@admin-node$ su - ceph; sudo ls -a /root should list files					
ceph@admin-node$ vim /etc/ssh/sshd_config
	PasswordAuthentication yes

ceph@admin-node$ ssh-keygen
ceph@admin-node$ ssh-copy-id ceph@node1
ceph@admin-node$ vim /etc/hosts
	192.168.1.1 admin-node
	192.168.1.2 node1
	192.168.1.3 node2
	192.168.1.4 node3
ceph@admin-node$ setenforce 0; yum -y install yum-plugin-priorities
ceph@admin-node$ yum update -y
ceph@admin-node$ sed -i 's/requiretty/\!requiretty/' /etc/sudoers # Allow remote sudo commands to run on all nodes
```

# Step 1: Deploy the Monitor Node
```sh
#  Add steps in this procedure are performed as user ceph
ceph@admin-node$ mkdir ceph-cluster; cd ceph-cluster
ceph@admin-node$ sudo yum install -y ceph-deploy
```

# Step 1: Install ceph-dploy on Ubuntu
```sh
$ wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -
$ echo deb http://ceph.com/debian-dumpling/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
$ sudo apt-get update
$ sudo apt-get install ceph-deploy
```

# Step 2: Install Software on all Nodes
```sh
ceph@all-node$ su - ceph
ceph@all-node$ mkdir ceph-cluster; cd ceph-cluster
ceph@all-node$ sudo yum install -y ceph-deploy
ceph@all-node$ ceph-deploy new osd-node1 osd-node2 osd-node3
ceph@all-node$ vim ceph.conf
	[global]
		mon_initial_members
ceph@all-node$ ceph-deploy install admin-node osd-node1 osd-node2 osd-node3
ceph@all-node$ ceph-deploy mon create-initial
```

# Step 2: Removing Ceph
```sh
$ ceph-deploy uninstall [hostname]
$ ceph-deploy purge [hostname]
```

# Step 2: Removing MON nodes
```sh
ceph-deploy mon destroy [hostname]
```

# Step (just action book): Deploy the ceph client configuration
```sh
ceph-deploy admin admin
```

# Step3: Prepare OSD Nodes in the Cluster
```sh
#  On all OSD nodes, make a dedicated block device available and format it with the XFS file systemc
#  Make a mount point on each node, and configure persistent mounting. Note that each node will have a diffrent directory name:
$ ceph-deploy disk zap osd-node?:sdb
ceph@osd-node$ fdisk /dev/sdb
	n
	p
	Enter
	w
ceph@osd-node$ mkfs.xfs /dev/sdb1
ceph@osd-node1$ mkdir -p /var/local/osd0
ceph@osd-node2$ mkdir -p /var/local/osd1
ceph@osd-node3$ mkdir -p /var/local/osd2
ceph@osd-node1$ echo "/dev/sdb1 /var/local/osd0 xfs noatime, nobarrier 0 0" >> /etc/fstab
ceph@osd-node2$ echo "/dev/sdb1 /var/local/osd1 xfs noatime, nobarrier 0 0" >> /etc/fstab
ceph@osd-node3$ echo "/dev/sdb1 /var/local/osd2 xfs noatime, nobarrier 0 0" >> /etc/fstab
ceph@osd-node$ mount -a: df -h
```

# Step4: Deploy Software to the OSD Nodes
```sh
Ceph OSD device role:
	system: OS storage for server running as OSD node
	journal: log of changes related to data resources, temporarity store data to be replicated across OSD nodes.
	Data: Storage resources

 $ ceph-deploy osd prepare osd-node1:/var/local/osd0
 $ ceph-deploy osd prepare osd-node2:/var/local/osd1
 $ ceph-deploy osd prepare osd-node3:/var/local/osd2
 $ ceph-deploy osd activate node1:/var/local/osd0 node2:/var/local/osd1 node3:/var/local/osd2
 $ ceph-deploy admin cephadmin node1 node2 node3
 $ sudo chmod +r /etc/ceph/ceph/client.admin.keyring
```

# Monitoring Status of the Cluster 

```sh
ceph -s
ceph -w
ceph health
ceph health detail

ceph@admin-node$ ceph-deploy disk list osd-node1
```

# (active book) Whoops, starting over
```sh
ceph-deploy purge {node-name}
ceph-doploy purgedate {node-name}
ceph-deploy forgetkeys

ceph-deploy purge admin-node mon-node1 osd-node1 osd-node2 osd-node3
ceph-deploy purgedata admin-node mon-node1 osd-node1 osd-node2 osd-node3
ceph-deploy forgetkeys
```