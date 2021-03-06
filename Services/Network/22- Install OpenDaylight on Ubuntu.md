## Install OpenDaylight on Ubuntu 20.04 LTS
```shell

sudo apt-get -y update && sudo apt-get -y upgrade

sudo apt-get -y install unzip openjdk-8-jre

sudo update-alternatives --config java
ls -l /etc/alternatives/java
lrwxrwxrwx 1 root root 46 Sep 27 20:24 /etc/alternatives/java -> /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre' >> ~/.bashrc
source ~/.bashrc
echo $JAVA_HOME

curl -XGET -O https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip
curl -XGET -O https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.12.2/karaf-0.12.2.zip
unzip karaf-0.8.4.zip
cd karaf-0.8.4/

./bin/karaf
feature:list


```
### How to install OpenDaylight as a Service on Ubuntu 18.04 LTS
```shell


sudo apt-get update
sudo apt-get -y install unzip vim wget openjdk-8-jre

sudo update-alternatives --config java

echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/' >> ~/.bashrc
source ~/.bashrc
echo $JAVA_HOME

wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip

sudo mkdir /usr/local/karaf
sudo mv karaf-0.8.4.zip /usr/local/karaf
sudo unzip /usr/local/karaf/karaf-0.8.4.zip -d /usr/local/karaf/
sudo update-alternatives --install /usr/bin/karaf karaf /usr/local/karaf/karaf-0.8.4/bin/karaf 1
sudo update-alternatives --config karaf
which karaf
/usr/bin/karaf

sudo -E karaf

feature:install odl-l2switch-switch
feature:install odl-mdsal-apidocs
feature:install odl-dlux-core
feature:install odl-dluxapps-topology
feature:install odl-dluxapps-nodes

feature:install  odl-dluxapps-yangui odl-dluxapps-yangvisualizer odl-dluxapps-yangman

feature:install odl-base-all odl-aaa-authn odl-restconf-all odl-nsf-all odl-adsal-northbound odl-ovsdb-northbound odl-ovsdb-openstack 
feature:install odl-l2switch-switch-ui 

sudo netstat -an | grep 8181

http://172.16.50.51:8181/index.html#/logi

system:shutdown

sudo update-alternatives --install /usr/bin/stop stop /usr/local/karaf/karaf-0.8.4/bin/stop 1
sudo update-alternatives --config stop
which stop

sudo vim /etc/systemd/system/opendaylight.service
[Unit]
Description=OpenDaylight Controller
After=network.target

[Service]
Type=simple
User=root
Group=root
Environment="JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/"
ExecStart=/usr/bin/karaf server
ExecStop=/usr/bin/stop
Restart=on-failure
RestartSec=60s

[Install]
WantedBy=multi-user.target

sudo chmod 0644 /etc/systemd/system/opendaylight.service
sudo systemctl daemon-reload
sudo systemctl enable opendaylight.service
sudo systemctl status opendaylight
sudo systemctl start opendaylight

ps -ef | grep karaf

```
### Mininet
```shell

sudo mn --controller=remote,ip=172.16.50.51,port=6633

feature:install odl-restconf
feature:install odl-l2switch-switch
feature:install odl-mdsal-apidocs
feature:install odl-dlux-all

mininet$ vim start-mininet-network.sh
sudo mn --topo linear,3 --mac --controller=remote,ip=127.0.0.1,port=6633 --switch ovs,protocols=openflow13
mininet$ ./start-mininet-network.sh

```
### Other
```shell

sudo update-alternatives --install /usr/bin/stop stop /usr/local/karaf/karaf-0.8.4/bin/stop 1
sudo update-alternatives --config stop
which stop

```