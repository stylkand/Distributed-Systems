# <b> NoobCash💰</b>
### A simple blockchain system in Python, semester project for Distributed Systems course at [ECE](https://www.ece.ntua.gr/en)⚡, [NTUA](https://www.ntua.gr/en)🎓, academic year 2021-2022

<img alt="Python" src = "https://img.shields.io/badge/Python-1136AA?style=for-the-badge&logo=python&logoColor=white" height="28"><img alt="Flask" src = "https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" height="28">


<hr>

## 📋**Description**

This repository contains an implementation of a simple **blockchain** system with **proof of work** consensus, named as **NoobCash**. The project was elaborated for the Distributed Systems course at ECE, NTUA, academic year 2021-2022.

**Details:**
- For our cluster we used 5 VMs.
- Every node is a miner too.
- Communication is achieved with Flask REST API
- A coordinator node is resposnible for bootstraping the system. After initial communication is established each client functions as an independent node.
- A CLI app provides user functionality, interacting in the background with the server by REST point requests.


Project's assignement and report are written in greek.

### 👔Team Members

| Name - GitHub                                     | Email                   |
|----------------------------------------------------------------|-------------------------|
| [Stylianos Kandylakis](https://github.com/stylkand/) | stelkcand@gmail.com    |
| [Kitsos Orfanopoulos](https://github.com/kitsorfan)               | <a href = "mailto:kitsorfan@protonmail.com" target="_blank"><img alt="protonamil" src = "https://img.shields.io/badge/ProtonMail-8B89CC?style=for-the-badge&logo=protonmail&logoColor=white" ></a>|
| [Christos Tsoufis](https://github.com/ChristosTsoufis)                 | el17176@gmail.com      |





## 🖥**Specifications of VM**

|OS | CPUs |RAM |Disk space|  
|----|-----|-------| ------|   
|Ubuntu 16.04 LTS (Xenial)| 2 | 2GB|30GB|


## 🛠**Installation Steps**

#### Install libraries 
```bash
apt-get install zlib1g-dev
```
```bash
apt-get install build-essential
```

#### Install python 3.6
```bash
cd /opt

wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz

tar -xvf Python-3.6.3.tgz

cd Python-3.6.3

./configure

make 

make install
```





#### Install python 3.6 (Alternatively)

```bash
sudo apt install python3.6
```

#### Install python3-venv

```bash
sudo apt-get install python3-venv
```

#### Create virtual environment

```bash
python3 -m venv env
```

#### Activate virtual environment

```bash
source env/bin/activate
```

#### Install packages

```bash
pip3 install -r requirements.txt
```



### **🔗Sources**
- https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/
- https://www.rosehosting.com/blog/how-to-install-python-3-6-on-ubuntu-16-04/
  
### **📑About README** 
<img alt="made with markdown" src ="https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg">

Learn more on READMEs:
- https://www.makeareadme.com/r
- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/



