# Scripting

### Q1: 

Option 1): Python script

0. `assumption all the remote connections have been setup, aka SSH keys`
1. `pip install parallel-ssh`
2. `python last_5_log.py -f hostFilePath`


Option 2): Ansbile playbook

`ansible-playbook -i yourInventory last_5_login.yml`

**or if no SSH key setup, you can use password as well**

`ansible-playbook -i yourInventory last_5_login.yml --ask-pass`

NOTE: probably using `ansible-vault` is a better way to manage all these passwords, and keys.

Option 3): Bash + CentOS

0. `sudo yum install pssh`
1. `pssh -i -h yourHostFile -- last -5`

NOTE: Assumign `yourHostFile` is in the following format:

```
user@hostname
user@ip
```

### Q2:

> Quick Start:

0. You need to have docker if you want to test inside a container, otherwise skip to step 
1. `./build.sh`
2. `./run.sh`
3. `./tomfinder.py -f test.log -s localhost`


### Q3: 

The purposes of the script was to find the following information: 
1. IP
2. Network Interface Controller
3. MAC address
4. Hostname

by creating 4 session variables and echo them out in the end.


# CI/CD

### Q1

Tools to use:
1. Any CI frontend tool (GitLab CI, Bamboo, Jenkins, Spinnaker, etc.). Any CI tool will do, don't have much of a preference. 
2. Docker itself. Well known container implementation
3. Private Registry (Nexus, Artifactory), or my new preference, GoHarbor, because it comes with built-in container vulnerability scanner. 


Typical workflow to push to production:
**Disclaimer: I don't have enough information for this "Docker project" to be comfortability to push anything to production**
> For any application to be promoted to production environment, here are the stuff I would consider: 

1. Do we have a working CI? (Build/Compile, Test (unit as well as integration), Versioning)
2. Is the application stateless or not?
3. Does this application have other dependencies? Third party or in-house applications.
4. If it is stateful, what database(s) does it use? Do we need de-indentify processes? Do we have a database backup, restoration or migration setup? Are they automated or manually handled? 
5. What are the deployment strategies? BigBang? Blue/Green? Rolling? Canary?

> For the purpose of this question, assuming we only care the flow of building, pushing, and deploying of this container. 

0. setup repo for this Docker project
1. setup CI pipeline which contains
* compile/build the code
* unit test
* if passed, tag the docker image
* push to private docker registry
2. setup CD pipeline, which includes
* got a trigger from the CI pipeline only on *master* branch
* could be as crude as a remote ssh call to trigger `docker pull` on the server to be deployed. Or perhaps trigger a custom deployment script depending on the complexity of the application

### Q2

My typical workflow: 

0. `git clone`
1. `git checkout master && git pull` # whenever I come back to this repo 
2. `git checkout -b local-master`    # depeneding on the build complexity of the project (in case there are tons of submodules, generated local artifacts after running Makefiles etc.), I'd prefer to have my experimental master branch 
3. `git checkout -b myFeatureBranch` # this is where my work begins 


--Now it is merging time, and assuming it has been a while--

Option 1):

1. `git add .` # or `git add onlyTheStuffIWant`
2. `git commit -m 'some stuff, obviously more meaningful when it is real work'`
3. `git push remoteOriginName myFeatureBranch` # in case there are multiple upstream
4. `create PR`

Option 2):

1. `git checkout master && git pull`
2. `git checkout myFeatureBranch`
3. `git rebase -i master`  # drop/pick/etc
4. `git commit -m 'rebase'`
5. `git push remoteOriginName myFeatureBranch`
6. `create PR`

Option 3):

1. `git checkout master && git pull`
2. `git checkout myFeatureBranch`
3. `git merge master`     # resolve conflicts if any
4. `git commit -m 'merge master'`
5. `git push remoteOriginName myFeatureBranch`
6. `create PR`

# Database

### SQL vs NoSQL

> In essence: NoSQL does not require Schema, whereas SQL has to comply with a pre-determined Schema.

Because of that, SQL exhibits `ACID` properties, where as NoSQL adhere to `CAP theorem`. [Reference](https://www.talend.com/resources/sql-vs-nosql/)

*ACID*:
* Atomicity means all transactions must succeed or fail completely. They cannot be partially-complete, even in the case of system failure.
* Consistency means that at each step the database follows invariants: rules which validate and prevent corruption.
* Isolation prevents concurrent transactions from affecting each other. Transactions must result in the same final state as if they were run sequentially, even if they were run in parallel.
* Durability makes transactions final. Even system failure cannot roll-back the effects of a successful transaction.

*CAP Theorem*
* Consistency: Every request receives the most recent result, or an error. (Note this is different than in ACID)
* Availability: Every request has a non-error result, regardless of how recent that result is.
* Partition tolerance: Any delays or losses between nodes will not interrupt the system’s operation.


#### How Data are stored

> For instance: 

**MongoDB**
MongoDB stores data as a `collection` of `documents`, but essentially, they are stored on disk.

Here is a sample query:

```javascript
db.inventory.find( {} ) // finds everything in the inventory collection
db.inventory.find( { status: "A", qty: { $lt: 30 } } ) // finds status = 'A', and qty less than 30
```

> And its equivalent queries in SQL are as following

**MySQL/MariaDB**

```SQL
SELECT * FROM inventory
SELECT * FROM inventory WHERE status in ("A", "D")
```
MySQL or similar RDBMS store data as a `tables` of `columns` and `rows`, but essentially, they are stored on disk.


# Scenario Based Question


### Q1

> This [OSQuery](https://osquery.io/) thing looks pretty cool as well ;) 

Possible bottlenecks. 

1. Server status

First thing first, I want to see if the underlying hardware/VM is healthy or not. 

A quick `uptime` would've given me a glimps into how many users are logged on and load-average trend so that I can have a quick estimate of how long has this been happening. 

For a much detailed real-time system status, I'd run `htop` or `top` to find out the exact CPU and RAM usage of the server.

On the network side, I'd run `iftop` to see ins-and-outs of all connections and its usage.


2. Apache configs

Check how many connections are connecting to the server through Apache right now with `sudo systemctl status -l httpd`

Check certain Apache configs to see if they are in an optimal state.

* Keep Alive Timeout (supposedly to be recommended between 1-5)
* Max Keep-Alive Requests (supposedly to be recommended around 500)
* Make sure `KeepAlive` is `On`
* Make sure multi-processing module is turned on with `sudo apachectl -t -D DUMP_MODULES |grep mpm`
* See if `HostnameLookups` is `On` or `Off`. It should be on so the midware won't spend extra resources jut to get a DNS name back each time.

All these configurations can be found in `/etc/httpd/conf`

3. MySQL performance

Use `mysqladmin proc stat` to log into the database and check a summary of how many `threads` are running, how many `opening` connections, and even number of `Slow queries`. 
Use `mysqldumpslow` to find the specific slow queries 


### Q2

1. SSL everywhere, ideally even within the company's network
2. Encrypt everything, everywhere. 
3. Firewall and IP whitelisting and filtering

### Q3

I'm not quite sure about the question, if the system is already in high load in production, then debugging a live application that's running in that hammered production environment is probably not a good idea. But I guess, I could do a `ps -elf` or `ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head` to find the high load, but non-application critical processes and kill them. Then start perusing the application logs to find where it went wrong. Potentially, even bring up another instance of the same application in a different server to see what's going on? Perhaps scale the application horizontally first before doing anything further just in case the application may crash anytime. 

### Q4

**Purly from IP's perspective**

1. Try `ping` from a few different servers in the same network space to see if areas other than the known unreachable servers can still communicate with the server to be checked. 
2. If luckily I found a server that I can still `ping` the "unreachable" servers, I will do a `traceroute` or `mtr` to that server from a server that can still talk to it, so that I can observe the routing table. Similarly, I would run `traceroute` or `mtr` on the certain areas that cannot reach this "unreachable" server, to see where the connection falls off. 
3. Adding the missing route *temporarily* to see if that would resolve the issue `ip route add missingRouteIP via someGateWayIP dev eth0`
4. Then modify `/etc/sysconfig/network-scripts/` with `missingRouteIP via someGateWayIP dev someInterface` 


**Now considering DNS**
Perhaps the server is reachable through IP not through FQDN. Then it's very likely to be an DNS issue. 

1. Check `/etc/resolv.conf` to see which DNS server those certain parts of the network that cannot reach to the servers are using. 
2. Validate from a healthy server to see if those DNS server names are valid. 
3. If they are not, fix it. But if they are, then follow the "IP's perspective" section above to troubleshoot what's going on with our DNS servers. 
