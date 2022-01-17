OpenHPC Install CentOS
======================


### 5.2. Login to Linux machine 
```
ssh root@master.haii.or.th
```

## 5.3. Prepare before installation 
--------------------------------

### add hosts file 
```
# vi /etc/hosts
192.168.1.254 master
```

### Turn off Firewall 
```
# systemctl disable firewalld
# systemctl stop firewalld
```

### Update the system
```
# yum -y update
# yum -y install wget
```

## 5.4 Install the OpenHPC repository
```
# yum -y install http://build.openhpc.community/OpenHPC:/1.3/CentOS_7/x86_64/ohpcrelease-1.3-1.el7.x86_64.rpm
```

## 5.5 Install OpenHPC Basic Package 
```
# yum -y install ohpc-base
# yum -y install ohpc-warewulf
```

## 5.6 Set Time Server to time.haii.or.th
```
# systemctl enable ntpd.service
# echo "server time.haii.or.th" >> /etc/ntp.conf
# systemctl restart ntpd
```

## 5.7 Install pb pro for Job Management 
```
# yum -y install pbspro-server-ohpc
```

## 5.8 Define internal interface, here use ens224
```
# perl -pi -e "s/device = eth1/device = enp0s3/" /etc/warewulf/provision.conf
```

## 5.9. Enable tftp service 
```
# perl -pi -e "s/^\s+disable\s+= yes/ disable = no/" /etc/xinetd.d/tftp
```

## 5.10 Assign ip to ens224
```
# ifconfig ens224 192.168.1.254 netmask 255.255.255.0 up
```

## 5.11 Restart the service in use. 
```
# systemctl restart xinetd
# systemctl enable mariadb.service
# systemctl restart mariadb
# systemctl enable httpd.service
# systemctl restart httpd
# systemctl enable dhcpd.service
```

## 5.12 Set the image for the compute node here as 
```
# export CHROOT=/opt/ohpc/admin/images/centos7.4
# wwmkchroot centos-7 $CHROOT
```

## 5.13 Install OpenHPC for compute node 
```
# yum -y --installroot=$CHROOT install ohpc-base-compute
```

## 5.14 Edit the resolv.conf file for the compute node. 
```
# cp -p /etc/resolv.conf $CHROOT/etc/resolv.conf
```

## 5.15. Install pbspro for compute node 

### set PBS_SERVER=master, clienthost master 
```
# yum -y --installroot=$CHROOT install pbspro-execution-ohpc
# perl -pi -e "s/PBS_SERVER=\S+/PBS_SERVER=master/" $CHROOT/etc/pbs.conf
# perl -pi -e "s/\$clienthost \S+/\$clienthost master/" $CHROOT/var/spool/pbs/mom_priv/config
# chroot $CHROOT opt/pbs/libexec/pbs_habitat
# echo "\$usecp *:/home /home" >> $CHROOT/var/spool/pbs/mom_priv/config
# chroot $CHROOT systemctl enable pbs
```

## 5.16. Install NTP for compute node 
```
# yum -y --installroot=$CHROOT install ntp
```

## 5.17. Install kernel for compute node 
```
# yum -y --installroot=$CHROOT install kernel
```

## 5.18. Install modules user environment for compute node 
```
# yum -y --installroot=$CHROOT install lmod-ohpc
```

## 5.19. Create OpenHPC Defaults 
```
# wwinit database
# wwinit ssh_keys
```

## 20. Create an NFS Client 
It mounts /home and /opt/ohpc/pub from 192.168.1.254(master).
```
# echo "192.168.1.254:/home /home nfs nfsvers=3,nodev,nosuid,noatime 0 0" >> $CHROOT/etc/fstab
# echo "192.168.1.254:/opt/ohpc/pub /opt/ohpc/pub nfs nfsvers=3,nodev,noatime 0 0" >> $CHROOT/etc/fstab
```

## 5.21. Create an NFS Server 
It will share /home and /opt/ohpc/pub. 
```
# echo "/home *(rw,no_subtree_check,fsid=10,no_root_squash)" >> /etc/exports
# echo "/opt/ohpc/pub *(ro,no_subtree_check,fsid=11)" >> /etc/exports
# exportfs -a
# systemctl restart nfs-server
# systemctl enable nfs-server
```

## 5.22. Configure kernel for compute node 
Point NTP at 192.168.1.254(master) machine. 
```
# chroot $CHROOT systemctl enable ntpd
# echo "server 192.168.1.254" >> $CHROOT/etc/ntp.conf
```

## 5.23. Configure memlock 
```
# perl -pi -e 's/# End of file/\* soft memlock unlimited\n$&/s' /etc/security/limits.conf
# perl -pi -e 's/# End of file/\* hard memlock unlimited\n$&/s' /etc/security/limits.conf
# perl -pi -e 's/# End of file/\* soft memlock unlimited\n$&/s' $CHROOT/etc/security/limits.conf
# perl -pi -e 's/# End of file/\* hard memlock unlimited\n$&/s' $CHROOT/etc/security/limits.conf
```

## 5.24. Configure the rsyslog of the compute node layer to the machine. 192.168.1.254(master) 
```
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

## 5.25. Install Ganglia for Monitor OpenHPC 
By setting <sms> = master and gridname to MySite.. 
```
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

## 5.26. Install Clustershell 
to adm: master 
Let compute: ${compute_prefix}[1-${num_computes}] where compute_prefix = c and num_computes = 2 
```
# yum -y install clustershell-ohpc
# cd /etc/clustershell/groups.d
# mv local.cfg local.cfg.orig
# echo "adm: master" > local.cfg
# echo "compute: c[1-2]" >> local.cfg
# echo "all: @adm,@compute" >> local.cfg
```

## 5.27. Import files used by OpenHPC 
```
# wwsh file list
# wwsh file import /etc/passwd
# wwsh file import /etc/group
# wwsh file import /etc/shadow
# wwsh file list
```

## 5.28. Configure the bootstrap image 
```
# export WW_CONF=/etc/warewulf/bootstrap.conf
# echo "drivers += updates/kernel/" >> $WW_CONF
# echo "drivers += overlay" >> $WW_CONF
```

## 5.29. Create a bootstrap image 
```
# wwbootstrap `uname -r`
```

## 5.30. Configure Virtual Node File System (VNFS) image 
```
# wwvnfs --chroot $CHROOT
```

## 5.31. Configure the value of the compute by MAC Address 
Let GATEWAYDEV=ens224 be a Public interface. 
```
# echo "GATEWAYDEV=enp0s8" > /tmp/network.$$
# wwsh -y file import /tmp/network.$$ --name network
# wwsh -y file set network --path /etc/sysconfig/network --mode=0644 --uid=0
# wwsh file list
```

We have 2 compute nodes c1 and c2. 
```
# wwsh -y node new c1 --ipaddr=192.168.1.253 --hwaddr=08:00:27:99:B3:4F -D enp0s8
# wwsh -y node new c2 --ipaddr=192.168.1.252 --hwaddr=08:00:27:99:B3:5F -D enp0s8
# wwsh node list
```
To delete a node, use the command wwsh node delete c1. 

## 5.32. Configure VNFS for compute node 
```
# wwsh -y provision set "c1" --vnfs=centos7.5 --bootstrap=`uname -r` --files=dynamic_hosts,passwd,group,shadow,network
# wwsh -y provision set "c2" --vnfs=centos7.5 --bootstrap=`uname -r` --files=dynamic_hosts,passwd,group,shadow,network
# wwsh provision list
```

## 5.33. Restart ganglia services due to added hostfile 
```
# systemctl restart gmond
# systemctl restart gmetad
# systemctl restart dhcpd
# wwsh pxe update
```

## 5.34. Determine the resources of the system 
We have Resources c1 and c2 machines. 
```
# systemctl enable pbs
# systemctl start pbs
# . /etc/profile.d/pbs.sh
# qmgr -c "set server default_qsub_arguments= -V"
# qmgr -c "set server resources_default.place=scatter"
# qmgr -c "set server job_history_enable=True"

# qmgr -c "create node c1"
# qmgr -c "create node c2"
# pbsnodes -a
```

## 5.35. Creating a User named test
```
# useradd -m test
# passwd test
# wwsh file resync
```

## 5.36. Install compute node with MAC Address as specified and boot from network as well. 
Challenge to turn on the compute node. When finished, you can check with pdsh command at the master machine. 
```
# pdsh -w c1 uptime
# pdsh -w c[1-2] uptime
```

## 5.37. Installing additional programs 
here let's install mpicc 
```
# yum -y install openmpi3-gnu7-ohpc mpich-gnu7-ohpc lmod-defaults-gnu7-openmpi3-ohpc
```

## 5.38. Test Interactive execution 
is a user named test 
```
# su - test
```

Compile MPI "hello world" example
```
$ mpicc -O3 /opt/ohpc/pub/examples/mpi/hello.c
```

Submit interactive job request
```
$ qsub -I -l select=2:mpiprocs=1
```

Use prun to launch executable
```
[test@c1 ~]$ prun ./a.out
[prun] Master compute host = c1
[prun] Resource manager = pbspro

[prun] Launch cmd = mpiexec -x LD_LIBRARY_PATH --prefix /opt/ohpc/pub/mpi/openmpi3-
gnu7/3.0.0 --hostfile /var/spool/pbs/aux/4.master ./a.out (family=openmpi3)

Hello, world (2 procs total)
 --> Process # 0 of 2 is alive. -> c1
 --> Process # 1 of 2 is alive. -> c2
 ```


## 5.39. Test Batch execution 
is a user named test 
```
# su - test
```

Copy sample job script from 
```
[test@master ~]$ cp /opt/ohpc/pub/examples/pbspro/job.mpi .
```

Modify the number of processors in use to #PBS -l select=2:mpiprocs=1
```
[test@master ~]$ vi job.mpi
#!/bin/bash
#----------------------------------------------------------
# Job name
#PBS -N test

# Name of stdout output file
#PBS -o job.out

# Total number of nodes and MPI tasks/node requested
#PBS -l select=2:mpiprocs=1

# Run time (hh:mm:ss) - 1.5 hours
#PBS -l walltime=01:30:00
#----------------------------------------------------------

# Change to submission directory
cd $PBS_O_WORKDIR

# Launch MPI-based executable
prun ./a.out
```

give Submit job for batch execution 
```
[test@master ~]$ qsub job.mpi
```

view job status 
```
[test@master ~]$ qstat
```

see result 
```
[test@master ~]$ cat job.out

[prun] Master compute host = c1
[prun] Resource manager = pbspro
[prun] Launch cmd = mpiexec -x LD_LIBRARY_PATH --prefix /opt/ohpc/pub/mpi/openmpi3-
gnu7/3.0.0 --hostfile /var/spool/pbs/aux/4.master ./a.out (family=openmpi3)


Hello, world (2 procs total)
 --> Process # 0 of 2 is alive. -> c1
 --> Process # 1 of 2 is alive. -> c2
 ```

 Web Ganglia can be viewed at http: http://192.168.11.6/ganglia/