```sh
ssh root@ceph-mon-01 

sudo vim /etc/hosts
127.0.0.1 localhost

# Ceph nodes
172.16.20.10  ceph-mon-01
172.16.20.11  ceph-mon-02
172.16.20.12  ceph-mon-03
172.16.20.13  ceph-osd-01
172.16.20.14  ceph-osd-02
172.16.20.15  ceph-osd-03

sudo apt update && sudo apt -y upgrade
sudo systemctl reboot

sudo apt update
sudo apt -y install software-properties-common git curl vim bash-completion ansible

echo "PATH=\$PATH:/usr/local/bin" >>~/.bashrc
source ~/.bashrc

$ ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa

curl --silent --remote-name --location https://github.com/ceph/ceph/raw/octopus/src/cephadm/cephadm
chmod +x cephadm
sudo mv cephadm  /usr/local/bin/

$ cephadm --help

cd ~/
vim prepare-ceph-nodes.yml
---
- name: Prepare ceph nodes
  hosts: ceph_nodes
  remote_user: cephadmin
  become: yes
  become_method: sudo
  vars:
    ceph_admin_user: cephadmin
  tasks:
    - name: Set timezone
      timezone:
        name: Asia/Tehran

    - name: Update system
      apt:
        name: "*"
        state: latest
        update_cache: yes

    - name: Install common packages
      apt:
        name: [vim,git,bash-completion,wget,curl,chrony]
        state: present
        update_cache: yes

    - name: Set authorized key taken from file to root user
      authorized_key:
        user: root
        state: present
        key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
   
    - name: Install Docker
      shell: |
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" > /etc/apt/sources.list.d/docker-ce.list
        apt update
        apt install -qq -y docker-ce docker-ce-cli containerd.io

    - name: Reboot server after update and configs
      reboot:

$ sudo vim /etc/ansible/hosts
[ceph_nodes]
ceph-mon-01
ceph-mon-02
ceph-mon-03
ceph-osd-01
ceph-osd-02
ceph-osd-03

eval `ssh-agent -s` && ssh-add ~/.ssh/id_rsa

tee -a ~/.ssh/config<<EOF
Host *
    UserKnownHostsFile /dev/null
    StrictHostKeyChecking no
    IdentitiesOnly yes
    ConnectTimeout 0
    ServerAliveInterval 300
EOF


$ ansible-playbook -i /etc/ansible/hosts prepare-ceph-nodes.yml --private-key ~/.ssh/id_rsa

ssh cephadmin@ceph-mon-02
sudo su -
logout
exit

vim update-hosts.yml
---
- name: Prepare ceph nodes
  hosts: ceph_nodes
  become: yes
  become_method: sudo
  tasks:
    - name: Clean /etc/hosts file
      copy:
        content: ""
        dest: /etc/hosts

    - name: Update /etc/hosts file
      blockinfile:
        path: /etc/hosts
        block: |
           127.0.0.1     localhost
           172.16.20.10  ceph-mon-01
           172.16.20.11  ceph-mon-02
           172.16.20.12  ceph-mon-03
           172.16.20.13  ceph-osd-01
           172.16.20.14  ceph-osd-02
           172.16.20.15  ceph-osd-03


$ ansible-playbook -i /etc/ansible/hosts update-hosts.yml --private-key ~/.ssh/id_rsa

sudo mkdir -p /etc/ceph
cephadm bootstrap \
  --mon-ip 172.16.20.10 \
  --initial-dashboard-user admin \
  --initial-dashboard-password Str0ngAdminP@ssw0rd

cephadm add-repo --release octopus
cephadm install ceph-common

ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph-mon-02
ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph-mon-03

ceph orch host label add ceph-mon-01 mon
ceph orch host label add ceph-mon-02 mon
ceph orch host label add ceph-mon-03 mon

ceph orch host add ceph-mon-02
ceph orch host add ceph-mon-03

ceph orch apply mon ceph-mon-02
ceph orch apply mon ceph-mon-03

ceph orch host ls

ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph-osd-01
ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph-osd-02
ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph-osd-03

ceph orch host add ceph-osd-01
ceph orch host add ceph-osd-02
ceph orch host add ceph-osd-03

ceph orch host label add  ceph-osd-01 osd
ceph orch host label add  ceph-osd-02 osd
ceph orch host label add  ceph-osd-03 osd

ceph orch daemon add osd ceph-osd-01:/dev/sdb
ceph orch daemon add osd ceph-osd-02:/dev/sdb
ceph orch daemon add osd ceph-osd-03:/dev/sdb

ceph -s
```
Source:
https://computingforgeeks.com/install-ceph-storage-cluster-on-ubuntu-linux-servers/