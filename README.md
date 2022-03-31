# <b> NoobCash💰</b>
### A simple blockchain system in Python, semester project for Distributed Systems course at [ECE](https://www.ece.ntua.gr/en)⚡, [NTUA](https://www.ntua.gr/en)🎓, academic year 2021-2022

<img alt="Python" src = "https://img.shields.io/badge/Python-1136AA?style=for-the-badge&logo=python&logoColor=white" height="28"> <img alt="Flask" src = "https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" height="28"> <img alt="Ubuntu Server" src = "https://img.shields.io/badge/Ubuntu Server-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" height="28">


<hr>

## 📋**Description**

This repository contains an implementation of a simple **blockchain** system with **proof of work** consensus, named as **NoobCash**. The project was elaborated for the Distributed Systems course at ECE, NTUA, academic year 2021-2022.

**Details:**
- We used 5 VMs for our cluster. Each VM had 1 or 2 threads, thus we had 5 or 10 nodes.
- Every node is a miner too.
- Communication is achieved with Flask REST API
- A coordinator node is resposnible for bootstraping the system. After initial communication is established each client functions as an independent node.
- A CLI app provides user functionality, interacting in the background with the server by REST point requests.


Project's assignement and report are written in greek.

### 👔Team Members

| Name - GitHub                                     | Email                   |
|----------------------------------------------------------------|-------------------------|
| [Stylianos Kandylakis](https://github.com/stylkand/) |  <a href = "mailto:stelkcand@gmail.com" target="_blank"><img alt="gmail" src = "https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white">   |
| [Kitsos Orfanopoulos](https://github.com/kitsorfan)               | <a href = "mailto:kitsorfan@protonmail.com" target="_blank"><img alt="protonmail" src = "https://img.shields.io/badge/ProtonMail-8B89CC?style=for-the-badge&logo=protonmail&logoColor=white" ></a>|
| [Christos Tsoufis](https://github.com/ChristosTsoufis)                 | <a href = "mailto:chris99ts@gmail.com" target="_blank"><img alt="gmail" src = "https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white">      |





## 🖥**Specifications of VM**

|OS | CPUs |RAM |Disk space|  
|----|-----|-------| ------|   
|Ubuntu 16.04 LTS (Xenial)| 2 | 2GB|30GB|


## 🛠**Installation Steps**

### Install libraries 
```bash
apt-get install zlib1g-dev
```
```bash
apt-get install build-essential
```

### Install python 3.6
```bash
cd /opt

wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz

tar -xvf Python-3.6.3.tgz

cd Python-3.6.3

./configure

make 

make install
```





### Install python 3.6 (Alternatively)

```bash
sudo apt install python3.6
```

### Install python3-venv

```bash
sudo apt-get install python3-venv
```

### Create virtual environment

```bash
python3 -m venv env
```

### Activate virtual environment

```bash
source env/bin/activate
```

### Install packages

```bash
pip3 install -r requirements.txt
```

### Automatically create requirements.txt
```bash
pip3 freeze > requirements.txt # for python3
```
## 💡**Execution Steps**
### Start flask server to each node
```bash
./noobcash.sh start 5000 
```
### Initialize bootstrap (only at predifined bootstrap node)
```bash
./noobcash.sh init 5 
```
### Connect every other node to the cluster
\<PORT\> and \<IP\> of current VM
```bash
./noobcash.sh connect <PORT> <IP> 
```


### **🔗Sources**
- [How to build a blockchain in Python](https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/)
- [How to install python 3.6 on Ubuntu](https://www.rosehosting.com/blog/how-to-install-python-3-6-on-ubuntu-16-04/)
- [Installing and using pip and virtual environment in Python](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
  
### **📑About README** 
<img alt="made with markdown" src ="https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg">

Learn more on READMEs:
- https://www.makeareadme.com/
- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/



