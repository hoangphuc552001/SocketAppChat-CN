from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import hashlib
import sys
clients = {}
addresses = {}
HOST = "127.0.0.1"
PORT = 8151
BUFSIZ = 4096
ADDR = (HOST, PORT)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)
SERVER_DATA_PATH = "server_data"    
SEPARATOR = "<SEPARATOR>"
USER_ONLINE_PATH="User_Online"
def register(conn,addr):
    user = conn.recv(BUFSIZ).decode("utf8")
    temp = user.split('@')
    if (temp[0]=='#yes'):
        user_no_encrypted=temp[1]
        user_encrypted=temp[2]
        passw_encrypted=temp[3]
        name_encrypted = temp[4]
        date_encrypted = temp[5]
        address_encrypted = temp[6]
        phone_encrypted =temp[7]
        note=temp[8]
        file=open(user_no_encrypted,"w")
        file.write(user_encrypted + "\n")
        file.write(passw_encrypted + "\n")
        file.write(name_encrypted + "\n")
        file.write(date_encrypted+"\n")
        file.write(address_encrypted+"\n")
        file.write(phone_encrypted+'\n')
        file.write(note)
        file.close()
    else:
        username = temp[0]
        password = temp[1]
        fullname = temp[2]
        date = temp[3]
        address=temp[4]
        phone=temp[5]
        note=temp[6]
        file = open(username,"w")
        file.write(username + "\n")
        file.write(password + "\n")
        file.write(fullname + "\n")
        file.write(date + '\n')
        file.write(address + '\n')
        file.write(phone+'\n')
        file.write(note)
        file.close()

def check_login(conn,addr):
    user = conn.recv(BUFSIZ).decode("utf8")
    temp = user.split()
    global username
    global password
    list_of_files = os.listdir()
    if (temp[0]=="no"):
        username = temp[1]
        password = temp[2]
        pass1=bytes(password,'utf8')
        passw = pass1.hex()
        if username in list_of_files:
            file1 = open(username, "r")
            verify = file1.read().splitlines()
            verify=str(verify[1]) 
            if str(password)== verify or passw==verify :
                conn.send(bytes("True","utf8"))
                filedestinationpath = os.path.join(USER_ONLINE_PATH,username)
                with open(filedestinationpath, "w") as f:
                    pass
                addresses[conn]=username
                return True
            else:
                conn.send(bytes("False","utf8"))
                return False

        else:
            conn.send(bytes("Wrong User","utf8"))
            return False
    else:
        byte_array = bytearray.fromhex(temp[1])
        username=byte_array.decode()     
        if str(username) in list_of_files:
            file1 = open(username, "r")
            verify = file1.read().splitlines()
            verify=str(verify[1])
            v1= bytes(verify,'utf8')
            v2=v1.hex()
            if  temp[2]== verify or temp[2]==v2 :
                conn.send(bytes("True","utf8"))
                filedestinationpath = os.path.join(USER_ONLINE_PATH,username)
                with open(filedestinationpath, "w") as f:
                    pass
                addresses[conn]=username
                return True
            else:
                conn.send(bytes("False","utf8"))
                return False

        else:
            conn.send(bytes("Wrong User","utf8"))
            return False


def accept_incoming_connections():
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = SOCK.accept()      
            print("%s:%s has connected." % client_address)
            while True:
                check = client.recv(BUFSIZ).decode("utf8")
                if check == "register":
                    register(client,client_address)
                elif check == "login":
                    while True:
                        flag = check_login(client,client_address)
                        if flag == True:
                            access = True
                            break
                    if access == True:
                        break
            # client.send("Greetings from the ChatRoom! ".encode("utf8"))
            # client.send("Now type your name and press enter!".encode("utf8"))
            addresses[client] = client_address

            Thread(target=handle_client, args=(client, client_address)).start()

def handle_client(conn, addr):  # Takes client socket as argument.
        """Handles a single client connection."""
        conn.send("Greetings from the ChatRoom! ".encode("utf8"))
        while True:
            check = conn.recv(BUFSIZ).decode("utf8")
            if "find" in check:
                t=check.split('@')
                user_name=t[1]
                list_of_files = os.listdir()
                if (user_name in list_of_files):
                    conn.send("True".encode("utf8"))
                else:
                    conn.send("False".encode("utf8"))
            elif "changepass" in check:
                t=check.split('@')
                id_user=t[1]
                passw=t[2]
                newpassw=t[3]
                pass1=bytes(passw,'utf8')
                passw_encrypted = pass1.hex()
                f=open(id_user,'r')
                strr=f.read()
                temp=strr.split('\n')
                f.close()
                if ((temp[1]==passw) or (temp[1]==passw_encrypted)):    
                    f1=open(id_user,"w")
                    f1.write(temp[0]+'\n')
                    f1.write(newpassw+'\n')
                    f1.write(temp[2]+'\n')
                    f1.write(temp[3 ]+'\n')
                    f1.write(temp[4]+'\n')
                    f1.write(temp[5]+'\n')
                    f1.write(temp[6])
                    f1.close()
                    conn.send("True".encode('utf8'))
                else:
                    conn.send("False".encode('utf8'))
            elif "check_online" in check:
                t=check.split('@')
                user_name=t[1]
                list_of_files = os.listdir()
                if (user_name in list_of_files):
                    list_user_online=os.listdir("User_Online")
                    if (user_name in list_user_online):
                        conn.send("True@Đang online".encode("utf8"))
                    else:
                        conn.send("True@Không đang online".encode("utf8"))
                else:
                    conn.send("False".encode("utf8"))
            elif "show_date" in check:
                t=check.split('@')
                user_name=t[1]
                list_of_files = os.listdir()
                if (user_name in list_of_files):
                    f=open(user_name,"r")
                    strr=f.read()
                    temp=strr.split('\n')
                    if (temp[0]=='Yes'):
                        send_mess="True"+'@'+temp[5]
                        conn.send(send_mess.encode("utf8"))
                    else:
                        send_mess="True"+'@'+temp[3]
                        conn.send(send_mess.encode("utf8"))
                else:
                    client.send("False".encode("utf8"))
            elif "show_name" in check:
                t=check.split('@')
                user_name=t[1]
                list_of_files = os.listdir()
                if (user_name in list_of_files):
                    f=open(user_name,"r")
                    strr=f.read()
                    temp=strr.split('\n')
                    if (temp[0]=='Yes'):
                        send_mess="True"+'@'+temp[4]
                        conn.send(send_mess.encode("utf8"))
                    else:
                        send_mess="True"+'@'+temp[2]
                        conn.send(send_mess.encode("utf8"))
                else:
                    conn.send("False".encode("utf8"))
            elif "show_note" in check:
                t=check.split('@')
                user_name=t[1]
                list_of_files = os.listdir()
                if (user_name in list_of_files):
                    f=open(user_name,"r")
                    strr=f.read()
                    temp=strr.split('\n')
                    if (temp[0]=='Yes'):
                        send_mess="True"+'@'+temp[8]
                        conn.send(send_mess.encode("utf8"))
                    else:
                        send_mess="True"+'@'+temp[6]
                        conn.send(send_mess.encode("utf8"))
                else:
                    conn.send("False".encode("utf8"))
            elif "show_all" in check:
                t=check.split('@')
                user_name=t[1]
                list_of_files = os.listdir()
                if (user_name in list_of_files):
                    f=open(user_name,"r")
                    strr=f.read()
                    temp=strr.split('\n')
                    if (temp[0]=='Yes'):
                        send_mess="True"+'@'+temp[4]+'@'+temp[5]+'@'+temp[6]+'@'+temp[7]+'@'+temp[8]
                        conn.send(send_mess.encode("utf8"))
                    else:
                        send_mess="True"+'@'+temp[2]+'@'+temp[3]+'@'+temp[4]+'@'+temp[5]+'@'+temp[6]
                        conn.send(send_mess.encode("utf8"))
                else:
                    conn.send("False".encode("utf8"))
            elif "setup_name" in check:
                t=check.split('@')
                user_name=t[1]
                f=open(user_name,"r")
                strr=f.read()
                temp=strr.split('\n')
                f.close()
                f1=open(user_name,"w")
                f1.write(temp[0]+'\n')
                f1.write(temp[1]+'\n')
                f1.write(t[2]+'\n')
                f1.write(temp[3]+'\n')
                f1.write(temp[4]+'\n')
                f1.write(temp[5]+'\n')
                f1.write(temp[6])
                f1.close()
            elif "setup_date" in check:
                t=check.split('@')
                user_name=t[1]
                f=open(user_name,"r")
                strr=f.read()
                temp=strr.split('\n')
                f.close()
                f1=open(user_name,"w")
                f1.write(temp[0]+'\n')
                f1.write(temp[1]+'\n')
                f1.write(temp[2]+'\n')
                f1.write(t[2]+'\n')
                f1.write(temp[4]+'\n')
                f1.write(temp[5]+'\n')
                f1.write(temp[6])
                f1.close()
            elif "stop" in check:
                break 
             
        files = os.listdir("User_Online")
        t=" , ".join(f for f in files)
        conn.send(bytes(t,"utf8")) 
        user_=conn.recv(BUFSIZ).decode("utf8")
        users=user_.split(',')
        for i in addresses:
            i.send(bytes(user_,'utf8'))  
        name = conn.recv(BUFSIZ).decode("utf8")
        welcome = 'Welcome %s! If you ever want to quit, type #quit to exit.' % name
        conn.send(bytes(welcome, "utf8"))
        msg = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(addr[0], addr[1]))
        broadcast(bytes(msg, "utf8"))
        clients[conn] = name
        while True:
                msg = conn.recv(BUFSIZ)
                temp=str(msg)
                upload="#upload"
                download="#download"
                m=msg.decode()
                if msg == bytes("Upload","utf8"):
                    pass
                elif msg== bytes("Download","utf8"):
                    conn.send(bytes("mời chọn file để download","utf8"))
                    files = os.listdir(SERVER_DATA_PATH)
                    if len(files) ==0:
                        conn.send(bytes("thư mục rỗng","utf8"))
                    else:
                        t=" , ".join(f for f in files)
                        conn.send(bytes(t,"utf8"))
                elif download in temp:
                    temp=temp.split(SEPARATOR)
                    filepath=temp[1]
                    pathmulti=filepath[0:len(filepath)-1]
                    if (filepath=="change_name"):
                        downLoad,changename,filename,filenewname,t=m.split(SEPARATOR)
                        filename=os.path.basename(filename)
                        try:
                            filedestinationpath = os.path.join(SERVER_DATA_PATH,filename)
                            i=0
                            with open(filedestinationpath, "rb") as f:
                                while True:
                                    bytes_read=f.read(BUFSIZ)
                                    i=i+1
                                    if not bytes_read:
                                        break
                            i=i-1
                            f.close()
                            conn.send(f"{download}{SEPARATOR}{filepath}{SEPARATOR}{filename}{SEPARATOR}{filenewname}{SEPARATOR}{i}{SEPARATOR}".encode()) 
                            with open(filedestinationpath,"rb") as f:
                                while True:
                                    bytes_read = f.read(BUFSIZ)
                                    if not bytes_read:    
                                        break
                                    conn.sendall(bytes_read)
                        except:
                            conn.send(bytes("không tồn tại file %s"% filedestinationpath,"utf8"))
                    elif filepath=="multi_files":
                        length=int(temp[2])
                        for i in range(length):
                            File=str(temp[i+4])
                            File=os.path.basename(File)
                            try:
                                filedestinationpath = os.path.join(SERVER_DATA_PATH,File)
                                j=0
                                with open(filedestinationpath, "rb") as f:
                                    while True:
                                        bytes_read=f.read(BUFSIZ)
                                        j=j+1
                                        if not bytes_read:
                                            break 
                                j=j-1
                                f.close()
                                if (j<=1):
                                    with open(filedestinationpath, "rb") as f:
                                        bytes_read=f.read(BUFSIZ)
                                    t=""
                                    conn.send(f"{download}{SEPARATOR}{filepath}{SEPARATOR}{File}{SEPARATOR}{j}{SEPARATOR}{t}".encode())
                                    t=conn.recv(BUFSIZ)
                                    conn.sendall(bytes_read)

                                else:
                                    t=""
                                    conn.send(f"{download}{SEPARATOR}{filepath}{SEPARATOR}{File}{SEPARATOR}{j}{SEPARATOR}{t}".encode())
                                    t=conn.recv(BUFSIZ)
                                    with open(filedestinationpath,"rb") as f:
                                        while True:
                                            bytes_read = f.read(BUFSIZ)
                                            if not bytes_read:    
                                                break
                                            conn.sendall(bytes_read)


                            except:
                                conn.send(bytes("không tồn tại file %s"% filedestinationpath,"utf8"))

                    else :
                        downLoad,filename,condition,t=m.split(SEPARATOR)
                        filename=os.path.basename(filename)
                        try:
                            filedestinationpath = os.path.join(SERVER_DATA_PATH,filename)
                            j=0
                            with open(filedestinationpath, "rb") as f:
                                while True:
                                    bytes_read=f.read(BUFSIZ)
                                    j=j+1
                                    if not bytes_read:
                                        break 
                            j=j-1
                            f.close()
                            conn.send(f"{download}{SEPARATOR}{filepath}{SEPARATOR}{filename}{SEPARATOR}{j}{SEPARATOR}{condition}{SEPARATOR}".encode()) 
                            if (condition=='no'):
                                with open(filedestinationpath,"rb") as f:
                                    while True:
                                        bytes_read = f.read(BUFSIZ)
                                        if not bytes_read:    
                                            break
                                        conn.sendall(bytes_read)
                            else:
                                with open(filedestinationpath,"rb") as f:
                                    strr1=""
                                    while True:
                                        bytes_read = f.read(BUFSIZ)
                                        if not bytes_read:    
                                            break
                                        strr=str(bytes_read.decode('utf8'))
                                        some_bytes=bytes(strr,'utf8')
                                        hexadecimal_string = some_bytes.hex()
                                        conn.sendall(bytes(hexadecimal_string,'utf8'))
                        except:
                            conn.send(bytes("không tồn tại file %s"% filedestinationpath,"utf8"))

                elif upload in temp:
                    temp=temp.split(SEPARATOR)
                    filepath=temp[1]
                    if (filepath=="multi_files"):
                        upload,multi,filename,line,t=m.split(SEPARATOR)
                        filename=os.path.basename(filename)
                        line=int(line)
                        filedestinationpath = os.path.join(SERVER_DATA_PATH,filename)
                        with open(filedestinationpath, "wb") as f:
                            for j in range(line):
                                bytes_read=conn.recv(4096)
                                if not bytes_read:
                                    break
                                f.write(bytes_read)
                        conn.send(bytes("upload file %s thành công"% filedestinationpath,"utf8"))
                    elif (filepath=="change_name"):
                        upload,changname,filename,filenewname,line,t=m.split(SEPARATOR)
                        filename=os.path.basename(filename)
                        line=int(line)
                        filedestinationpath=os.path.join(SERVER_DATA_PATH,filenewname)
                        with open(filedestinationpath,"wb") as f:
                            for j in range(line):
                                bytes_read=conn.recv(4096)
                                if not bytes_read:
                                    break
                                f.write(bytes_read)
                                f.flush()
                        conn.send(bytes("upload file %s thành công"% filedestinationpath,"utf8"))
                    else:
                        upload,filename,filesize,check=m.split(SEPARATOR)
                        filename=os.path.basename(filename)
                        filesize=int(filesize)
                        filedestinationpath = os.path.join(SERVER_DATA_PATH,filename)
                        if (check=='yes'):
                            with open(filedestinationpath,"wb") as f:
                                    bytes_read=conn.recv(BUFSIZ)
                                    strr=str(bytes_read.decode('utf8'))
                                    byte_array = bytearray.fromhex(strr)
                                    ch=byte_array.decode()
                                    ch1=bytes(ch,'utf8')
                                    f.write(ch1)
                        else:
                            with open(filedestinationpath,"wb") as f:
                                    bytes_read=conn.recv(BUFSIZ)
                                    f.write(bytes_read)
                        conn.send(bytes("upload file %s thành công"% filedestinationpath,"utf8")) 
                elif msg != bytes("#quit", "utf8"):
                    broadcast(msg, name + ": ")
                else:
                    conn.send(bytes("#quit", "utf8"))
                    conn.close()
                    del clients[conn]
                    broadcast(bytes("%s has left the chat." % name, "utf8"))
                    break


def broadcast(msg, prefix=""):  # prefix is for name identification.
        """Broadcasts a message to all the clients."""
        for sock in clients:
            sock.send(bytes(prefix, "utf8") + msg)
if __name__ == "__main__":
        SOCK.listen(5)  # Listens for 5 connections at max.
        print("Chat Server has Started !!")
        print("Waiting for connections...")
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        ACCEPT_THREAD.start()  # Starts the infinite loop.
        ACCEPT_THREAD.join()
        SOCK.close()