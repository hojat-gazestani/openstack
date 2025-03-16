Host name
---------
# Ceph nodes
172.16.30.104   sm0	
172.16.30.106   sm1
172.16.30.105   sm2
172.16.30.100   sr0
172.16.30.103   sr1
172.16.30.102   sr2

sudo hostnamectl set-hostname sm0

SSH configuration
-----------------
sudo useradd -d /home/ceph-admin -m ceph-admin -s /bin/bash
echo 'ceph-admin:openstack' | sudo chpasswd # useradd ceph; echo openstack | passwd --stdin ceph
echo "ceph-admin ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ceph-admin
sudo chmod 0440 /etc/sudoers.d/ceph-admin

ssh-keygen

tee -a ~/.ssh/config <<EOF
Host *
   UserKnownHostsFile /dev/null
   StrictHostKeyChecking no
   IdentitiesOnly yes
   ConnectTimeout 0
   ServerAliveInterval 300
Host sr0
   Hostname sr0
   User ceph-admin
   UserKnownHostsFile /dev/null
   StrictHostKeyChecking no
   IdentitiesOnly yes
   ConnectTimeout 0
   ServerAliveInterval 300
Host sr1
   Hostname sr1
   User ceph-admin
   UserKnownHostsFile /dev/null
   StrictHostKeyChecking no
   IdentitiesOnly yes
   ConnectTimeout 0
   ServerAliveInterval 300
Host sr2
   Hostname sr2
   User ceph-admin
   UserKnownHostsFile /dev/null
   StrictHostKeyChecking no
   IdentitiesOnly yes
   ConnectTimeout 0
   ServerAliveInterval 300
EOF

su ceph-admin
ssh-keygen
ssh-copy-id ceph-admin@sr0 && ssh-copy-id ceph-admin@sr1 && ssh-copy-id ceph-admin@sr2
for i in sr0 sr1 sr2; do
    ssh-copy-id $i
done

Network Time Protocol NTP
-------------------------
sudo apt install chrony -y

sudo vim /etc/chrony/chrony.conf
server _NTP_SERVER_ iburst
allow 172.16.50.0/24

sudo vim /etc/chrony/chrony.conf
server _controller01_ iburst

sudo systemctl enable chronyd.service
sudo systemctl start chronyd.service

sudo chronyc sources

timedatectl													

User Configuration
------------------
setenforce 0; yum -y install yum-plugin-priorities
yum update -y
sed -i 's/requiretty/\!requiretty/' /etc/sudoers # Allow remote sudo commands to run on all nodes
