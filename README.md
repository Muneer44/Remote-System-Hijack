# Remote System-Hijack Program.

> ### _The Remote System-Hijack Program is a Backdoor application, which gives complete control over a remote system._


## Notice
This application is a Proof of Concept [PoC] to understand how a malicious file is built and used, This is purely intended for educational purposes. Do not use it to compromise any unauthorized device, demonstrate only on your own devices.
# 

## Demonstration
![Backdoor](https://user-images.githubusercontent.com/31078414/201514766-c8566a7a-3fff-4576-b135-d15d8bd103f3.gif)
> The Kali Linux VM on the left is playing the attacker (listener), and on the right, the Windows-11 VM machine is the target.

## This repository contains:
- **Backdoor.py :** Request connection and enable remote access 
- **Listener.py :** Establish incoming reverse connection from target system

## Capabilities:
- Connect 2 systems remotely
- Send and receive data over TCP
- Execute system commands on remote system
- Download files from remote system
- Upload files to the remote system.
- Cross-platform program

_This application is tested and tried on Python 3.10.7 and works on more than one computer architecture/ OS._

## Installation process
clone this repository with `git clone`, configure `backdoor.py` arguments, execute the `listener.py` file on local system and `backdoor.py` file on target system.
```
user@host:~$ git clone https://github.com/Muneer44/remote-system-hijack.git
user@host:~$ cd Remote-System-Hijack
```
*Update parameters in the backdoor.py file :* _listener's `IP` and `Port`_
```
C:\Users\user> python3 "Remote-System-Hijack/backdoor.py" 
user@host:~$ sudo python3 "Remote-System-Hijack/listener.py -i <listener's Ip> -p <port> 
```

## Mitigations
- Limit open network ports
- Use complex system password
- Apply strict firewall rules
- Restrict file uploads on web server
- implement strong input validation on web application
- Use anti-malware softwares
- Stay on top of security updates/ patches

## Disclaimer
The use of code contained in this repository, either in part or in its totality,
for engaging targets without prior mutual consent is illegal. **It is
the end user's responsibility to obey all applicable local, state and
federal laws.**

> NOTE: This application is deliberately not packaged into an executable (Trojan) to avoid malicious usage.

