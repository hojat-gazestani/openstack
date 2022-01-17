How to install OpenHPC and Slurm On CentOS
==========================================

### Login to linux server
```commandline
ssh root@192.168.1.254
```

5.3. Prepare to install.
------------------------

### Edit hosts file.
```commandline
# vi /etc/hosts
192.168.1.254 master
164.115.20.65 build.openhpc.community
```

### Disable Firewall.
```commandline
# systemctl disable firewalld
# systemctl stop firewalld
```

### Update system.
```commandline
# yum -y update
# yum -y install wget
```

5.4. Installation Repository of OpenHPC.
----------------------------------------
```commandline
# yum -y install http://build.openhpc.community/OpenHPC:/1.3/CentOS_7/x86_64/ohpc-
release-1.3-1.el7.x86_64.rpm
```

### 5.5. Install Basic Package of OpenHPC.
```commandline
# yum -y install ohpc-base
# yum -y install ohpc-warewulf
```

###5.6. Edit Time Server configuration add servername time.haii.or.th.
```commandline
# systemctl enable ntpd.service
# echo "server time.haii.or.th" >> /etc/ntp.conf
# systemctl restart ntpd
```

### 5.7. Install Sluarm for Job scheduling and workload management.
```commandline
# yum -y install ohpc-slurm-server
# perl -pi -e "s/ControlMachine=\S+/ControlMachine=master/" /etc/slurm/slurm.conf
```

### 5.8. Configure internal interface. Replace eth1 by ens224.
```commandline
# perl -pi -e "s/device = eth1/device = ens224/" /etc/warewulf/provision.conf
```

### 5.9. Enable tftp service.
```commandline
# perl -pi -e "s/^\s+disable\s+= yes/ disable = no/" /etc/xinetd.d/tftp
```

### 5.10. Up ip interface enp0s3.
```commandline
# ifconfig enp0s3 192.168.1.254 netmask 255.255.255.0 up
```

### 5.11. Restart services all service.
```commandline
# systemctl restart xinetd
# systemctl enable mariadb.service
# systemctl restart mariadb
# systemctl enable httpd.service
# systemctl restart httpd
# systemctl enable dhcpd.service
```

### 5.12. Define image location for compute node. Use /opt/ohpc/admin/images/centos7.4
```commandline
# export CHROOT=/opt/ohpc/admin/images/centos7.4
# wwmkchroot centos-7 $CHROOT
```

### 5.13. Install OpenHPC for compute node.
```commandline
# yum -y --installroot=$CHROOT install ohpc-base-compute
```

### 5.14. create resolv.conf file for compute node.
```commandline
# cp -p /etc/resolv.conf $CHROOT/etc/resolv.conf
```

### 5.15. Install slurm client in image compute node.
```commandline
# yum -y --installroot=$CHROOT install ohpc-slurm-client
```

### 5.16. Install NTP for compute node.
```commandline
# yum -y --installroot=$CHROOT install ntp
```

### 5.17. Install kernel for compute node.
```commandline
# yum -y --installroot=$CHROOT install kernel
```

### 5.18. Install modules user environment for compute node.
```commandline
# yum -y --installroot=$CHROOT install lmod-ohpc
```

### 5.19. Initialize warewulf database for OpenHPC.
```commandline
# wwinit database
# wwinit ssh_keys
```

### 5.20. Create NFS Client for compute node.
mount /home and /opt/ohpc/pub from 192.168.1.254(master)
```commandline
# echo "192.168.1.254:/home /home nfs nfsvers=3,nodev,nosuid,noatime 0 0" >> $CHROOT/etc/fstab
# echo "192.168.1.254:/opt/ohpc/pub /opt/ohpc/pub nfs nfsvers=3,nodev,noatime 0 0" >> $CHROOT/etc/fstab
```

### 5.21. Create NFS Server.
Share directory /home and /opt/ohpc/pub on 192.168.1.254(master)
```commandline
# echo "/home *(rw,no_subtree_check,fsid=10,no_root_squash)" >> /etc/exports
# echo "/opt/ohpc/pub *(ro,no_subtree_check,fsid=11)" >> /etc/exports
# exportfs -a
# systemctl restart nfs-server
# systemctl enable nfs-server
```

### 5.22. Setup NTP on compute node.
Add NTP server 192.168.1.254(master) to compute node.
```commandline
# chroot $CHROOT systemctl enable ntpd
# echo "server 192.168.1.254" >> $CHROOT/etc/ntp.conf
```

### 5.23. Update basic slurm configuration.
slurm client node have 2 node is c1 and c2. And vCPU is 2 core/nodes.
```commandline
# perl -pi -e "s/^NodeName=(\S+)/NodeName=c[1-2]/" /etc/slurm/slurm.conf
# perl -pi -e "s/^PartitionName=normal Nodes=(\S+)/PartitionName=normal Nodes=c[1-2]/" /etc/slurm/slurm.conf
# perl -pi -e "s/^Sockets=(\S+)/Sockets=1/" /etc/slurm/slurm.conf
# perl -pi -e "s/^CoresPerSocket=(\S+)/CoresPerSocket=2/" /etc/slurm/slurm.conf
# perl -pi -e "s/^ThreadsPerCore=(\S+)/ThreadsPerCore=1/" /etc/slurm/slurm.conf
# perl -pi -e "s/^NodeName=(\S+)/NodeName=c[1-2]/" $CHROOT/etc/slurm/slurm.conf
# perl -pi -e "s/^PartitionName=normal Nodes=(\S+)/PartitionName=normal Nodes=c[1-2]/" $CHROOT/etc/slurm/slurm.conf
# perl -pi -e "s/^Sockets=(\S+)/Sockets=1/" $CHROOT/etc/slurm/slurm.conf
# perl -pi -e "s/^CoresPerSocket=(\S+)/CoresPerSocket=2/" $CHROOT/etc/slurm/slurm.conf
# perl -pi -e "s/^ThreadsPerCore=(\S+)/ThreadsPerCore=1/" $CHROOT/etc/slurm/slurm.conf
# systemctl enable munge
# systemctl enable slurmctld
# systemctl start munge
# systemctl start slurmctld
# chroot $CHROOT systemctl enable slurmd
```

### 5.24. Increase locked memory limits.
```commandline
# perl -pi -e 's/# End of file/\* soft memlock unlimited\n$&/s' /etc/security/limits.conf
# perl -pi -e 's/# End of file/\* hard memlock unlimited\n$&/s' /etc/security/limits.conf
# perl -pi -e 's/# End of file/\* soft memlock unlimited\n$&/s' $CHROOT/etc/security/limits.conf
# perl -pi -e 's/# End of file/\* hard memlock unlimited\n$&/s' $CHROOT/etc/security/limits.conf
```

Enable slurm pam module
```commandline
# echo "account required
pam_slurm.so" >> $CHROOT/etc/pam.d/sshd
```

### 5.25. rsyslog setup.
In compute node set rsyslog config to 192.168.1.254(master).
```commandline
# perl -pi -e "s/\\#\\\$ModLoad imudp/\\\$ModLoad imudp/" /etc/rsyslog.conf
# perl -pi -e "s/\\#\\\$UDPServerRun 514/\\\$UDPServerRun 514/" /etc/rsyslog.conf
# systemctl restart rsyslog
# echo "*.* @192.168.1.254:514" >> $CHROOT/etc/rsyslog.conf
# perl -pi -e "s/^\*\.info/\\#\*\.info/" $CHROOT/etc/rsyslog.conf
# perl -pi -e "s/^authpriv/\\#authpriv/" $CHROOT/etc/rsyslog.conf
# perl -pi -e "s/^mail/\\#mail/" $CHROOT/etc/rsyslog.conf
# perl -pi -e "s/^cron/\\#cron/" $CHROOT/etc/rsyslog.conf
# perl -pi -e "s/^uucp/\\#uucp/" $CHROOT/etc/rsyslog.conf
```

### 5.26. Install Ganglia Monitor OpenHPC.
change <sms> to master and gridname to MySite..
```commandline
# yum -y install ohpc-ganglia
# yum -y --installroot=$CHROOT install ganglia-gmond-ohpc
# cp /opt/ohpc/pub/examples/ganglia/gmond.conf /etc/ganglia/gmond.conf
# perl -pi -e "s/<sms>/master/" /etc/ganglia/gmond.conf
# cp /etc/ganglia/gmond.conf $CHROOT/etc/ganglia/gmond.conf
# echo "gridname MySite.." >> /etc/ganglia/gmetad.conf
# systemctl enable gmond
# systemctl enable gmetad
# systemctl start gmond
# systemctl start gmetad
# chroot $CHROOT systemctl enable gmond
# systemctl try-restart httpd
```

### 5.27. Add Clustershell.
add role adm to masteradd role compute to ${compute_prefix}[1-${num_computes}] by compute_prefix = c and
num_computes = 2
```commandline
# yum -y install clustershell-ohpc
# cd /etc/clustershell/groups.d
# mv local.cfg local.cfg.orig
# echo "adm: master" > local.cfg
# echo "compute: c[1-2]" >> local.cfg
# echo "all: @adm,@compute" >> local.cfg
# cd
```

### 5.28. Import files.
```commandline
# wwsh file list
# wwsh file import /etc/passwd
# wwsh file import /etc/group
# wwsh file import /etc/shadow
# wwsh file import /etc/slurm/slurm.conf
# wwsh file import /etc/munge/munge.key
# wwsh file list
```

### 5.29. Assemble bootstrap image.
````commandline
# export WW_CONF=/etc/warewulf/bootstrap.conf
# echo "drivers += updates/kernel/" >> $WW_CONF
# echo "drivers += overlay" >> $WW_CONF
````

### 5.30. Build bootstrap image.
```commandline
# wwbootstrap `uname -r`
```

### 5.31. create Virtual Node File System(VNFS) image.
```commandline
# wwvnfs --chroot $CHROOT
```

### 5.32. Define compute node from MAC Address.
GATEWAYDEV=enp0s8 is Public interface.
```commandline
# echo "GATEWAYDEV=enp0s8" > /tmp/network.$$
# wwsh -y file import /tmp/network.$$ --name network
# wwsh -y file set network --path /etc/sysconfig/network --mode=0644 --uid=0
# wwsh file list
```

Have 2 compute node include c1 and c2. Add to warewulf data store.
```commandline
# wwsh -y node new c1 --ipaddr=192.168.1.253 --hwaddr=08:00:27:99:B3:4F -D enp0s8
# wwsh -y node new c2 --ipaddr=192.168.1.252 --hwaddr=08:00:27:99:B3:5F -D enp0s8
# wwsh node list
```
**if you need delete node. use command “wwsh node delete c1”.

### 5.33. Defind VNFS to compute node.
```commandline
# wwsh -y provision set "c1" --vnfs=centos7.4 --bootstrap=`uname -r` --files=dynamic_hosts,passwd,group,shadow,slurm.conf,munge.key,network
# wwsh -y provision set "c2" --vnfs=centos7.4 --bootstrap=`uname -r` --files=dynamic_hosts,passwd,group,shadow,slurm.conf,munge.key,network
# wwsh provision list
```

### 5.34. Restart ganglia/dhcp services
```commandline
# systemctl restart gmond
# systemctl restart gmetad
# systemctl restart dhcpd
# wwsh pxe update
```

### 5.35. Create usersname test
```commandline
# useradd -m test
# passwd test
# wwsh file resync
# updatenode compute -F
```

### 5.36. Power On compute node have correct MAC Address and first boot fromnetwork.
Power On compute node and test by pdsh command on master node.
```commandline
# pdsh -w c1 uptime
# pdsh -w c[1-2] uptime
```

### 5.37. Resource Manager Startup.
```commandline
# systemctl restart munge
# systemctl restart slurmctld
# pdsh -w c[1-2] systemctl restart slurmd
```

Test mung by
```commandline
# munge -n | unmunge
# munge -n | ssh c1 unmunge
# munge -n | ssh c2 unmunge
```

Test slurm by
```commandline
# systemctl status slurmctld
# ssh c1 systemctl status slurmd
# ssh c2 systemctl status slurmd
```

Test resource by
```commandline
# scontrol show nodes
```
See State=IDLE. Resource is good. else State Please run

scontrol update NodeName=c1 State=Resume

### 5.38. Compilers
Install mpicc compiler.
```commandline
# yum -y install openmpi3-gnu7-ohpc mpich-gnu7-ohpc lmod-defaults-gnu7-openmpi3-ohpc
```

### 5.39. Test Interactive execution.
su to test user.
```commandline
# su - test
```

Compile MPI "hello world" example
```commandline
$ mpicc -O3 /opt/ohpc/pub/examples/mpi/hello.c
```

Submit interactive job request. n=mpi tasks and N=nodes.
```commandline
$ srun -n 2 -N 1 --pty /bin/bash
```

Use prun to launch executable
```commandline
[test@c1 ~]$ prun ./a.out
[prun] Master compute host = c1
[prun] Resource manager = slurm
[prun] Launch cmd = mpirun ./a.out (family=openmpi3)

Hello, world (2 procs total)

--> Process # 0 of 2 is alive. -> c1
--> Process # 1 of 2 is alive. -> c1
```

5.40. Test Batch execution.
--------------------------
su to test user.
````commandline
# su - test
````

Copy sample job script from /opt/ohpc/pub/examples/pbspro/job.mpi
```commandline
[test@master ~]$ cp /opt/ohpc/pub/examples/slurm/job.mpi .
```

edit -n to 1 for mpi tasks and N to 2 for nodes.
````commandline
[test@master ~]$ vi job.mpi
#!/bin/bash

#SBATCH -J test
# Job name
#SBATCH -o job.%j.out # Name of stdout output file (%j expands to jobId)
#SBATCH -N 1 # Total number of nodes requested
#SBATCH -n 2 # Total number of mpi tasks requested
#SBATCH -t 01:30:00 # Run time (hh:mm:ss) - 1.5 hours

# Launch MPI-based executable

prun ./a.out
````

Submit job for batch execution by sbatch
```commandline
[test@master ~]$ sbatch job.mpi
```

Job status command. by squeue.
```commandline
[test@master ~]$ squeue
```

Job output.
```commandline
[test@master ~]$ cat job.XX.out
[prun] Master compute host = c1
[prun] Resource manager = slurm
[prun] Launch cmd = mpirun ./a.out (family=openmpi3)

Hello, world (2 procs total)
--> Process # 0 of 2 is alive. -> c1
--> Process # 1 of 2 is alive. -> c1
```

Delete job = scancel [job id]
job status = scontrol show job
node status = scontrol show node

Open Web Ganglia at http://192.168.11.6/ganglia/