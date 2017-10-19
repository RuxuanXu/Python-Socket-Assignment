import socket
import configparser

IRCSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config = configparser.ConfigParser()
config.read('Config.ini')

host = str(config['config']['host'])
port = int(config['config']['port'])
channel = str(config['config']['channel'])
password = str(config['config']['password'])
botname = str(config['config']['botname'])
admin = str(config['config']['admin'])

IRCSocket.connect((host, 6667))

def join(ch,pwd):
    IRCSocket.send(bytes("USER "+ botname +" "+ botname +" "+ botname + " " + botname + "\n", "UTF-8")) # user information
    IRCSocket.send(bytes("NICK "+ botname +"\n", "UTF-8"))
    IRCSocket.send(bytes("JOIN "+ ch +" " + pwd + "\n", "UTF-8"))
    msg=""
    while msg.find("End of /NAMES list.") == -1:
        msg = IRCSocket.recv(1024).decode("UTF-8")
        print(msg)
    IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+"Hello! I am Meow Bot written by Ruxuan Xu."+"\n", "UTF-8"))

def repeat(msg, ch):
    msg = msg.split('PRIVMSG',1)[1].split(':',1)[1]
    msg = msg.split('@repeat',1)[1].split(' ',1)[1]
    IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ msg +"\n", "UTF-8"))

def convert(num, ch):
    num = num.split('PRIVMSG',1)[1].split(':',1)[1]
    num = num.split('@convert',1)[1].split(' ',1)[1]
    try:
      int(num,10)
      IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ hex(int(num)) +"\n", "UTF-8"))
    except ValueError:
      try:
        int(num,16)
        IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ str(int(num,16)) +"\n", "UTF-8"))
      except ValueError:
        IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ "Please input decimal or hexadecimal." +"\n", "UTF-8")) 

def validate(ip):
    try:
        socket.inet_aton(ip)
        return 1
    except socket.error:
        return 0

def ipcalc(ip, ch):
    ip = ip.split('PRIVMSG',1)[1].split(':',1)[1]
    ip = ip.split('@ip',1)[1].split(' ',1)[1]
    if len(ip)>12:
        IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ "0" +"\n", "UTF-8"))
        return 0
    validnum = 0
    validip = []
    n = [1,2,3]
    for a in n:
        for b in n:
            for c in n:
                temp = ip[:a]+'.'+ ip[a:a+b]+'.'+ip[a+b:a+b+c]+'.'+ip[a+b+c:]
                if validate(temp):
                    validnum += 1
                    validip.append(temp)
    IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ str(validnum) +"\n", "UTF-8"))
    for i in validip:
        IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ i +"\n", "UTF-8"))

def bothelp(ch):
    IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ "@repeat <Message>" +"\n", "UTF-8"))
    IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ "@convert <Number>" +"\n", "UTF-8"))
    IRCSocket.send(bytes("PRIVMSG "+ ch +" :"+ "@ip <String>" +"\n", "UTF-8"))

def main():
    
  join(channel,password)
  while 1:
    msg = IRCSocket.recv(4096).decode("UTF-8")
    msg = msg.strip('\n\r')
    print(msg)
    if msg.find("@repeat") != -1:
        repeat(msg, channel)
    if msg.find("@convert") != -1:
        convert(msg, channel)
    if msg.find("@ip") != -1:
        ipcalc(msg, channel)
    if msg.find("@help") != -1:
        bothelp(channel)
    if msg.find("PING :") != -1:
        IRCSocket.send(bytes("PONG :pingis\n", "UTF-8"))
        
main()
 
