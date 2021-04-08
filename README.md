# SquidNet
A highly functional Botnet with security, powerful bot scripts, and the ability to set up remote access to it with admin scripts along with an ugly web-interface. It is mainly using TCP for regular bots, but it can use SSH when logging into SSH Servers.

# Features:
Security - Has a Username and Password that the user is able to configure, to set up remote connections.

Web-Interface - Ability to view connections and general info about the server via a webpage

Option-Parsing - Re-usability and having the ability to configure the server with only one cmd command.

Bots - Compromised Bots infected with the Bot script will connect to the server(if configured correctly), and are able to do many different things.

Remote-Connections - Ability to set-up remote connections with admins, so that the server can also be used remotely via an admin.

SSH Compatability - The botnet can also take control of SSH Servers.

Logging - The server is logged, and server errors can be checked there.

Smart-Script-Generation - The Botnet will generate Bot and Admin scripts on command.

# Security:

The Botnet will be able to determine whether a bot is a bot or not. There is a custom command for being recognized by the botnet. If that command is not recieved, the incoming connection will be closed, and they will be kicked. If they do enter the correct command, they will be recognized as a proper client of the Botnet. If an admin is connecting to the Botnet, they will send the login command to the server, and also send the command that allows them access. They will need to enter the correct username or password, otherwise they will be kicked and the server will be warned. During password configuration(sorry for going a little off topic), the provided username will be put in a txt file, as well as the password. However, this password will first be hashed with the md5 hashing algorythm for increased security. Back to the admins connections, the username and password will be checked with the txt file with the correct credentials. The password in the command will first be hashed, and it will be checked with what is in the text file. If the username and password are correct, they will be granted access to the server.

Example of the Admin-File:

![adminfile](/ex1.png)

Warn-Message:

![warnmsg](/ex6.png)

Bot Being Recognized:

![botmsg](/ex8.png)

# Web-Interface

The Botnet has a web-interface for when the user wants to see the connections in a more simpler format. The web-interface will be able to show the connections in a table, where it is much easier to read, as well as showing information about them. In the tables, you are able to see the hostname of who is connected, the IP Address, the username of the connection, the source port(good for differentiate between duplicate connections), as well as the os. The main connections are listed in the first table, and the admin connections are listed in the second. For the SSH Connections, those are listed in the 3rd table. They will have the hostname first, then the IP Address, and finally the password of the SSH Server. Then there will be some other information about the configured variables in the Botnet. These include where the log file is located, the IP and Port used to connect to the Botnet, the admin login info, Encryption Key for encrypting files on the bots, and also the bruteforcing password-list for ssh connections. It doesn't look too great, as I am not very knowledgeable when it comes to HTML. 

Example of the Web-Interface:

![webinterface](/ex2.png)

# Option-Parsing

The Botnet uses option-parsing to configure settings in the Botnet. This can include the host IP and the host Port that the server will be hosted, as well as the admin username and the admin password(optional, as the defaults are 'admin' and 'root'). You will need to specify a password list text file, otherwise the help message will display. If you are on a windows machine, you can get ngrok using '--gN' and it will download ngrok for windows in your current directory. You can also do '--i' for displaying the help message. You can also specify an encryption key, however there is a default key set meaning that it is optional. You are also able to specify external ip addresses and ports, if you want to.

Help Message:

![helpmsg](/ex3.png)

Example of Option-Parsing:

![optparseex](/ex4.png)

# Bots

The Bots are the computers used to connect to the server and run commands from it. These can do many things, as there are many commands in the server that can be ran in the bots. One of the main commands that it can do is that it can conduct DDoS Attacks. There are 3 types of DDoS Attacks possible with the bot script, one being an HTTP Flood attack which floods a web server with seeming legitimate HTTP Requests, which would then take the web server down and make it unavailable. Theres a TCP Flood attack that floods TCP Servers with packets, as well as a UDP Flood Attack doing similar things like the TCP Flooder. There are also custom commands that can be ran in the bots, some including google password obtaining(only for windows bots), as well as the ability to edit files remotely and also run cmd commands on the bots from the Botnet or the admins. There are many commands that are able to be used on the Bots, but I will not explain them here. For the SSH Bots, you can run cmd commands, with administrator privalleges and also able to be injected with files with SFTP, however this can only happen via the main Botnet. The bots will reconnect if they are disconnected from the Botnet.

Commands List:

![cmdlist](/ex5.png)

# Remote-Connections

These are for admin connections. The admins are able to do nearly every command in the server, where they could also start DDoS Attacks and also run cmd commands remotely. When they do provide the correct username and passwords(this is explained more in the Security section), they will have access to the Botnet and all of the Bots that are connected to it. When it is connected, the admin will get sent the command list of what commands are able to be used remotely, and also how to use them. If the admin gets disconnected for some reason, they will be able to reconnect to the server rather quickly(depending on if its down or not).

Admin Connection Being Announced:

![adminconn](/ex7.png)

# SSH-Compatibility

The Botnet is able to setup SSH Connections for SSH Bots. It can do this from either brute-forcing from a passwordlist(It's really slow, I suggest using another tool like hydra), or logging in directly with a provided password. If the SSH Credentials are able to be cracked, you are able to remotely access the SSH Server's shell and are able to run commands for it remotely at an administrative privallage. There is an additional command for if you want to inject a file to the SSH Bots, which you can get a file from the Botnet's working directory and can send it directly to the Bots via SFTP(Secure File Transfer Protocol).

SSH-Password Cracked Broadcast:

![sshconn](/ex9.png)

# Logging

(Writing in progress)

# Smart-Script-Generation

(Writing in progress)
