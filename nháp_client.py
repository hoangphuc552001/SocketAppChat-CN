import os
from tkinter import*
import tkinter
from tkinter import messagebox
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import hashlib
import tkinter.messagebox
SEPARATOR = "<SEPARATOR>"
CLIENT_DATA_PATH = "client_data_upload"
CLIENT_DATA_PATH1 = "client_data_download"

HOST = "127.0.0.1"
PORT = 8151
BUFSIZ = 4096
ADDR = (HOST, PORT)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)
def receive():
    """ Handles receiving of messages. """
    while True:
        try:
            msg = sock.recv(BUFSIZ)
            m=msg.decode()
            temp=str(msg)
            download="#download"
            if download in temp:
                temp=temp.split(SEPARATOR)
                check=temp[1]
                if(check=="change_name"):
                    download,change,file,newfile,line,t=m.split(SEPARATOR)
                    line=int(line)
                    file=os.path.basename(file)
                    newfile=os.path.basename(newfile)
                    filedestinationpath = os.path.join(CLIENT_DATA_PATH1,newfile)
                    with open(filedestinationpath, "wb") as f:
                        for j in range(line):
                            bytes_read=sock.recv(4096)
                            if not bytes_read:
                                break
                            f.write(bytes_read)
                    msg_list.insert(tkinter.END, "download file %s thành công"%filedestinationpath)
                elif(check=="multi_files"):
                    download,multi,file,line,t=m.split(SEPARATOR)
                    sock.send(bytes('123','utf8'))
                    line=int(line)
                    file=os.path.basename(file)
                    filedestinationpath = os.path.join(CLIENT_DATA_PATH1,file)
                    strr=str(t)
                    strr=strr[2:len(strr)-1]
                    s=bytes(strr,'utf8')
                    if (line<=1):
                        with open(filedestinationpath, "wb") as f:
                            msg = sock.recv(BUFSIZ)
                            f.write(msg) 
                    else:
                        with open(filedestinationpath, "wb") as f:
                            for j in range(line):   
                                bytes_read=sock.recv(4096)
                                if not bytes_read:
                                    break
                                f.write(bytes_read)
                         

                    msg_list.insert(tkinter.END, "download file %s thành công"%filedestinationpath)
                else:
                    download,filepath,file,line,condition,t=m.split(SEPARATOR)
                    line=int(line)
                    file=os.path.basename(file)
                    filedestinationpath = os.path.join(CLIENT_DATA_PATH1,file)
                    if condition=='yes':
                        with open(filedestinationpath, "wb") as f:
                            for j in range(line):
                                bytes_read=sock.recv(4096)
                                if not bytes_read:
                                    break
                                strr=str(bytes_read.decode('utf8'))
                                byte_array = bytearray.fromhex(strr)
                                ch=byte_array.decode()
                                ch1=bytes(ch,'utf8')
                                f.write(ch1)
                    else:
                        with open(filedestinationpath, "wb") as f:
                            for j in range(line):
                                bytes_read=sock.recv(4096)
                                if not bytes_read:
                                    break
                                f.write(byte_array)

                    msg_list.insert(tkinter.END, "download file %s thành công"%filedestinationpath)
            else:
                ms=msg.decode("utf8")
                msg_list.insert(tkinter.END, ms)
        except OSError:  # Possibly client has left the chat.
            break
def send(event=None):
    """ Handles sending of messages. """
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    temp_msg=msg
    temp=str(msg)
    if msg != "#quit":
        msg=msg.split(" ")
        cmd=msg[0]
        if cmd !="#upload" and cmd!="#download":
            sock.send(bytes(temp, "utf8"))
        elif cmd=="#download":
            cmd1=msg[1]
            if cmd1=="change_name":
                sock.send(f"{cmd}{SEPARATOR}{cmd1}{SEPARATOR}{msg[2]}{SEPARATOR}{msg[3]}{SEPARATOR}".encode()) 
            elif cmd1=="multi_files":
                strr=cmd+SEPARATOR+cmd1
                length=len(msg)-2
                text=""
                for i in range(length):
                    text+=SEPARATOR+msg[i+2]
                sock.send(f"{strr}{SEPARATOR}{str(length)}{SEPARATOR}{text}{SEPARATOR}".encode())
            else:
                root=tkinter.Tk()
                canvas1 = tkinter.Canvas(root, width = 300, height = 300)
                canvas1.pack()
                def Application():
                    MsgBox = tkinter.messagebox.askquestion ('Mã hóa file','Bạn có muốn mã hóa file?',icon = 'warning')
                    path=CLIENT_DATA_PATH+'/'+msg[1]
                    filename = path.split("/")[-1]
                    sock.send(f"{cmd}{SEPARATOR}{filename}{SEPARATOR}{MsgBox}{SEPARATOR}".encode())
                    root.destroy()
                button1 = tkinter.Button (root, text='Mã hóa file',command=Application,bg='brown',fg='white')
                canvas1.create_window(150, 150, window=button1)

        else:
            cmd1=msg[1]
            if cmd1 =="change_name":
                cmd2=msg[3]
                path=CLIENT_DATA_PATH+'/'+msg[2]
                filename = path.split("/")[-1]
                i=0
                with open(path,"rb") as f:
                    while True:
                        bytes_read=f.read(BUFSIZ)
                        i=i+1
                        if not bytes_read:
                            break  
                i=i-1
                f.close()
                sock.send(f"{cmd}{SEPARATOR}{cmd1}{SEPARATOR}{filename}{SEPARATOR}{cmd2}{SEPARATOR}{i}{SEPARATOR}".encode()) 
                with open(path,"rb") as f:
                    while True:
                        bytes_read = f.read(BUFSIZ)
                        if not bytes_read:    
                            break
                        sock.sendall(bytes_read)
            elif cmd1=="multi_files":
                numberoffiles=len(msg)-2
                for i in range(numberoffiles):
                    path=CLIENT_DATA_PATH+'/'+msg[i+2]
                    filename = path.split("/")[-1]
                    j=0
                    with open(path,"rb") as f:
                        while True:
                            bytes_read=f.read(BUFSIZ)
                            j=j+1
                            if not bytes_read:
                                break  
                    j=j-1
                    f.close()
                    sock.send(f"{cmd}{SEPARATOR}{cmd1}{SEPARATOR}{filename}{SEPARATOR}{j}{SEPARATOR}".encode()) 
                    print(j) 
                    with open(path,"rb") as f:
                        while True:
                            bytes_read = f.read(BUFSIZ)
                            if not bytes_read:    
                                break
                            sock.sendall(bytes_read)
                    f.close()
            else:
                root=tkinter.Tk()
                canvas1 = tkinter.Canvas(root, width = 300, height = 300)
                canvas1.pack()
                def Application():
                    MsgBox = tkinter.messagebox.askquestion ('Mã hóa file','Bạn có muốn mã hóa file?',icon = 'warning')
                    path=CLIENT_DATA_PATH+'/'+msg[1]
                    filename = path.split("/")[-1]
                    filesize = os.path.getsize(path)
                    sock.send(f"{cmd}{SEPARATOR}{filename}{SEPARATOR}{filesize}{SEPARATOR}{MsgBox}".encode())
                    root.destroy()
                    if MsgBox=='no':
                        with open(path,"rb") as f:
                            bytes_read = f.read(BUFSIZ)
                            sock.sendall(bytes_read)
                    else:
                        with open(path,"rb") as f:
                                content=""
                                bytes_read = f.read(BUFSIZ)
                                strr=str(bytes_read.decode('utf8'))
                                some_bytes=bytes(strr,'utf8')
                                hexadecimal_string = some_bytes.hex()
                                sock.sendall(bytes(hexadecimal_string,'utf8'))
                button1 = tkinter.Button (root, text='Mã hóa file',command=Application,bg='brown',fg='white')
                canvas1.create_window(150, 150, window=button1)
    


    else:
        msg=msg.split(" ")
        cmd=msg[0]
        if cmd == "#quit":
            sock.close()
            top.quit()
       

 

def on_closing(event=None):
    """ This function is to be called when the window is closed. """
    my_msg.set("#quit")
    send()

def Hello(event=None):
    my_msg.set("Hello")    
    send()

def Goodbye(event=None):
    my_msg.set("Goodbye")   
    send()
def Upload(event=None):
    my_msg.set("Upload")
    msg="Mời chọn file để upload:"
    msg_list.insert(tkinter.END, msg)
    files = os.listdir(CLIENT_DATA_PATH)
    if len(files) ==0:
        msg_list.insert(tkinter.END, "thư mục rỗng")
    else:
        t=" , ".join(f for f in files)
        msg_list.insert(tkinter.END,t)
    send()
def Download(event=None):
    my_msg.set("Download")
    send()
#login
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    sock.send(bytes("register","utf8"))
    register_screen.title("Register")
    register_screen.geometry("300x370")
 
    global username
    global password
    global username_entry
    global password_entry
    global fullname
    global fullname_entry
    global date 
    global date_entry
    global address
    global address_entry
    global phone_number
    global phone_number_entry
    global note 
    global note_entry
    username = StringVar()
    password = StringVar()
    fullname = StringVar()
    date =StringVar()
    address=StringVar()
    phone_number=StringVar()
    note=StringVar()
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    fullname_lable = Label(register_screen, text="Fullname  ")
    fullname_lable.pack()
    fullname_entry = Entry(register_screen, textvariable=fullname)
    fullname_entry.pack()
    date_lable = Label(register_screen, text="Date of birth  ")
    date_lable.pack()
    date_entry = Entry(register_screen, textvariable=date)
    date_entry.pack()
    address_lable = Label(register_screen, text="Address  ")
    address_lable.pack()
    address_entry = Entry(register_screen, textvariable=address)
    address_entry.pack()
    phone_number_lable = Label(register_screen, text="Phone Number  ")
    phone_number_lable.pack()
    phone_number_entry = Entry(register_screen, textvariable=phone_number)
    phone_number_entry.pack()
    note_lable = Label(register_screen, text="Note  ")
    note_lable.pack()
    note_entry = Entry(register_screen, textvariable=note)
    note_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()

 
# Designing window for login 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    sock.send(bytes("login","utf8"))
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
 
# Implementing event on register button
 
def register_user():
    username_info = username.get()
    password_info = password.get()
    fullname_info = fullname.get()
    date_info = date.get()
    address_info=address.get()
    phone_number_info=phone_number.get()
    note_info=note.get()
    root=tkinter.Tk()
    canvas1 = tkinter.Canvas(root, width = 300, height = 300)
    canvas1.pack()
    def Application():
        MsgBox = tkinter.messagebox.askquestion ('Mã hóa','Bạn có muốn mã hóa tài khoản?',icon = 'warning')
        if (MsgBox=='no'):
            user = username_info + "@" + password_info + "@" + fullname_info + "@"+date_info+"@"+address_info+"@"+phone_number_info+'@'+note_info
            sock.send(bytes(user,"utf-8"))
            Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
            root.destroy()
        else:
            user1=bytes(username_info,'utf8')
            user = user1.hex()
            pass1=bytes(password_info,'utf8')
            passw = pass1.hex()
            data_sended = "#yes"+"@"+username_info+"@"+user+ "@" + passw+ "@" + fullname_info + "@"+date_info+"@"+address_info+"@"+phone_number_info+'@'+note_info
            sock.send(bytes(data_sended,"utf-8"))
            Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
            root.destroy()


    button1 = tkinter.Button (root, text='Mã hóa tài khoản',command=Application,bg='brown',fg='white')
    canvas1.create_window(150, 150, window=button1)

 
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    fullname_entry.delete(0,END)
    date_entry.delete(0,END)
    phone_number_entry.delete(0,END)
    address_entry.delete(0,END)
    note_entry.delete(0,END)
# Implementing event on login button 
 
def login_verify():
    global username1
    username1 = username_verify.get()
    password1 = password_verify.get()
    MsgBox = tkinter.messagebox.askquestion ('Mã hóa','Bạn có muốn mã hóa login?',icon = 'warning')
    if (MsgBox=='no'):
        user = MsgBox+" "+username1 + " " + password1
        sock.send(bytes(user,"utf8"))
    else:
        user1=bytes(username1,'utf8')
        user = user1.hex()
        pass1=bytes(password1,'utf8')
        passw = pass1.hex()
        user_send = MsgBox+" "+ user + " " + passw
        sock.send(bytes(user_send,"utf8"))
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    check = sock.recv(BUFSIZ).decode("utf8")
    if check == "True":
        login_sucess()
    elif check == "False":
        password_not_recognised()
    elif check == "Wrong User":
        user_not_found()
 
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()
    login_screen.destroy()
    main_screen.destroy()
 
# Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
  
def delete_login_success():
    login_success_screen.destroy()
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
def delete_user_not_found_screen():
    user_not_found_screen.destroy() 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login,activeforeground="red",activebackground="pink").pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register,activeforeground="red",activebackground="pink").pack()
    main_screen.mainloop()
def Find():
    global check_user_string
    check_user_string=User.get()
    cmd='find'+'@'+check_user_string
    sock.send(bytes(cmd,'utf8'))
    check=sock.recv(BUFSIZ).decode("utf8")
    if (check=='True'):
        noti = Tk()  
        noti.title("Notification")  
        Label(noti, text="Tồn tại user").grid(column=0,row=0,padx=20,pady=30)  
    else:
        messagebox.showwarning('Notification','Không tồn tại user')

   
def Online():
    global show_online_user
    show_online_user=User.get()
    cmd='check_online'+'@'+show_online_user
    sock.send(bytes(cmd,'utf8'))
    check=sock.recv(BUFSIZ).decode("utf8")
    if ("True" in check):
        check_=check.split('@')
        online_user=check_[1]
        noti = Tk()  
        noti.title("Notification")  
        Label(noti, text=online_user).grid(column=0,row=0,padx=20,pady=30)  
    else:
        messagebox.showwarning('Notification','Không tồn tại user')
def Show_date():
    global show_date_string
    show_date_string=User.get()
    cmd='show_date'+'@'+show_date_string
    sock.send(bytes(cmd,'utf8'))
    check=sock.recv(BUFSIZ).decode("utf8")
    if ("True" in check):
        check_=check.split('@')
        date_user=check_[1]
        noti = Tk()  
        noti.title("Notification")  
        Label(noti, text="Date of birth: "+date_user).grid(column=0,row=0,padx=20,pady=30)  
    else:
        messagebox.showwarning('Notification','Không tồn tại user')


def Show_name():
    global show_name_string
    show_name_string=User.get()
    cmd='show_name'+'@'+show_name_string
    sock.send(bytes(cmd,'utf8'))
    check=sock.recv(BUFSIZ).decode("utf8")
    if ("True" in check):
        check_=check.split('@')
        date_user=check_[1]
        noti = Tk()  
        noti.title("Notification")  
        Label(noti, text="Full Name: "+date_user).grid(column=0,row=0,padx=20,pady=30)  
    else:
        messagebox.showwarning('Notification','Không tồn tại user')

def Show_note():
    global show_note_string
    show_note_string=User.get()
    cmd='show_note'+'@'+show_note_string
    sock.send(bytes(cmd,'utf8'))
    check=sock.recv(BUFSIZ).decode("utf8")
    if ("True" in check):
        check_=check.split('@')
        date_user=check_[1]
        noti = Tk()  
        noti.title("Notification")  
        Label(noti, text="Note: "+date_user).grid(column=0,row=0,padx=20,pady=30)  
    else:
        messagebox.showwarning('Notification','Không tồn tại user')
def Show_all():
    global show_all_string
    show_all_string=User.get()
    cmd='show_all'+'@'+show_all_string
    sock.send(bytes(cmd,'utf8'))
    check=sock.recv(BUFSIZ).decode("utf8")
    if ("True" in check):
        check_=check.split('@')
        date_user=check_[1]+'\n'+check_[2]+'\n'+check_[3]+'\n'+check_[4]+'\n'+check_[5]
        noti = Tk()  
        noti.title("Notification")  
        Label(noti, text="Information: "+date_user).grid(column=0,row=0,padx=20,pady=30)  
    else:
        messagebox.showwarning('Notification','Không tồn tại user')
def name_change_user():
    global setup_name
    setup_name=name_change.get()
    cmd='setup_name'+'@'+username1+'@'+setup_name
    sock.send(bytes(cmd,'utf8'))
    messagebox.showinfo("Info", "Setup thành công")
    setup_name_screen.destroy()
def setup_name():
    global setup_name_screen
    global name_change
    name_change=StringVar()
    setup_name_screen = Toplevel(main_lobby)
    setup_name_screen.geometry("200x120")
    setup_name_screen.title("Setup Name")
    Label(setup_name_screen, text="Mời nhập tên muốn setup").pack()
    Label(setup_name_screen, text="").pack()
    global username_entry
    username_entry = Entry(setup_name_screen, textvariable=name_change)
    username_entry.pack()
    Button(setup_name_screen, text="OK", width=10, height=1,command=name_change_user).pack()
def date_change_user():
    global setup_date
    setup_date=date_change.get()
    cmd='setup_date'+'@'+username1+'@'+setup_date
    sock.send(bytes(cmd,'utf8'))
    messagebox.showinfo("Info", "Setup thành công")
    setup_date_screen.destroy()
def setup_date():
    global setup_date_screen
    global date_change
    date_change=StringVar()
    setup_date_screen = Toplevel(main_lobby)
    setup_date_screen.geometry("200x120")
    setup_date_screen.title("Setup Name")
    Label(setup_date_screen, text="Mời nhập date muốn setup").pack()
    Label(setup_date_screen, text="").pack()
    global username_entry
    username_entry = Entry(setup_date_screen, textvariable=date_change)
    username_entry.pack()
    Button(setup_date_screen, text="OK", width=10, height=1,command=date_change_user).pack()
def setup_info():
    global check_user_screen
    global User
    User=StringVar()
    check_user_screen = Toplevel(main_lobby)
    check_user_screen.geometry("200x150")
    check_user_screen.title("Setup User")
    Label(check_user_screen, text="").pack()
    Button(check_user_screen, text="Full Name", width=10, height=1,command=setup_name).pack()
    Label(check_user_screen, text="").pack()
    Button(check_user_screen, text="Date", width=10, height=1,command=setup_date).pack()
def check_user():
    global check_user_screen
    global User
    User=StringVar()
    check_user_screen = Toplevel(main_lobby)
    check_user_screen.geometry("250x360")
    check_user_screen.title("Check User")
    Label(check_user_screen, text="Mời nhập tên user").pack()
    Label(check_user_screen, text="").pack()
    global username_entry
    username_entry = Entry(check_user_screen, textvariable=User)
    username_entry.pack()
    Label(check_user_screen, text="").pack()
    Button(check_user_screen, text="Find", width=10, height=1,command=Find).pack()
    Label(check_user_screen, text="").pack()
    Button(check_user_screen, text="Online", width=10, height=1,command=Online).pack()
    Label(check_user_screen, text="").pack()
    Button(check_user_screen, text="Show date", width=10, height=1,command=Show_date).pack()
    Label(check_user_screen, text="").pack()
    Button(check_user_screen, text="Show_name", width=10, height=1,command=Show_name).pack()
    Label(check_user_screen, text="").pack()
    Button(check_user_screen, text="Show_note", width=10, height=1,command=Show_note).pack()
    Label(check_user_screen, text="").pack()
    Button(check_user_screen, text="Show_all", width=10, height=1,command=Show_all).pack()
def send_user():
    users_request=user_request.get()
    ids_room=id_room.get()
    passs_room=pass_room.get()
    sock.send(bytes(ids_room+','+passs_room+','+users_request,'utf8'))
    if (users_request!="#"):
        room_screen.destroy()
        main_lobby.destroy()
    else:
        check=sock.recv(BUFSIZ).decode("utf8")
        if (check=="True"):
            room_screen.destroy()
            main_lobby.destroy()
        else:
            messagebox.showwarning('Notification','Wrong password')
            room_screen.destroy()

def check_pass():
    MsgBox = tkinter.messagebox.askquestion ('Mã hóa','Bạn có muốn mã hóa password?',icon = 'warning')
    oldpass1 = oldpass.get()
    newpass1 = newpass.get()
    newpass2=bytes(newpass1,'utf8')
    newpass_encrypted=newpass2.hex() 
    if (MsgBox=='no'): 
        sock.send(bytes('changepass'+'@'+username1+'@'+oldpass1+'@'+newpass1,'utf8'))
    else:
        sock.send(bytes('changepass'+'@'+username1+'@'+oldpass1+'@'+newpass_encrypted,'utf8'))
    check=sock.recv(BUFSIZ).decode("utf8")
    if (check=='True'):
        messagebox.showinfo("Notification", "Change password thành công")
    else:
        messagebox.showwarning('Notification','Wrong password')

def changepass():
    global Change_password
    global oldpass
    global oldpass_entry
    global newpass
    global newpass_entry
    oldpass = StringVar()
    newpass = StringVar()
    Change_password = Toplevel(main_lobby)
    Change_password.geometry("200x150")
    Change_password.title("Change Password")
    Label(Change_password, text="Old pass * ").pack()
    oldpass_entry = Entry(Change_password, textvariable=oldpass,show='*')
    oldpass_entry.pack()
    Label(Change_password, text="").pack()
    Label(Change_password, text="Password * ").pack()
    newpass_entry = Entry(Change_password, textvariable=newpass, show= '*')
    newpass_entry.pack()
    Label(Change_password, text="").pack()
    Button(Change_password, text="OK", width=10, height=1, command = check_pass).pack()
def join_room():
    sock.send(bytes('#join','utf8'))    
    noti.destroy()
    main_lobby.destroy()
def wait():
    global noti
    noti = Toplevel(main_lobby)
    noti.geometry("200x300")
    noti.title("User Request")
    check=sock.recv(BUFSIZ).decode("utf8")
    split_=check.split(',')
    room_id=split_[0]
    pass_id=split_[1]
    if (username1 in check):
        Label(noti, text="Bạn có lời mời từ room "+room_id).pack()
        Label(noti, text="").pack()
        Label(noti, text="Password "+pass_id).pack()
        Label(noti, text="").pack()
        sock.send(bytes('stop','utf8'))    
        Button(noti, text="OK", width=10, height=1, command = join_room).pack()
    else:
        pass
def create_room():
    sock.send(bytes('stop','utf8'))    
    global room_screen
    global user_request
    global users_request
    global room_screen_entry
    global id_room
    global pass_room    
    user_request=StringVar()
    id_room=StringVar()
    pass_room=StringVar()
    room_screen = Toplevel(main_lobby)
    room_screen.geometry("400x600")
    room_screen.title("User Online")
    Label(room_screen,text="User Online", width="200",height="2",font =("Calibri",13)).pack()
    user_online=sock.recv(BUFSIZ).decode("utf8")
    users=user_online.split(',')
    length=len(users)
    for i in range(length):
        Label(room_screen,text="").pack()
        Label(room_screen,text=users[i]+'\n', width="200",height="2",font =("Calibri",13)).pack()
    Label(room_screen, text="Users you want to join group chat:").pack()
    room_screen_entry = Entry(room_screen, textvariable=user_request)
    room_screen_entry.pack()
    Label(room_screen, text="Nhập id phòng:").pack()
    id_screen_entry = Entry(room_screen, textvariable=id_room)
    id_screen_entry.pack()
    Label(room_screen, text="Nhập pass phòng:").pack()
    pass_screen_entry = Entry(room_screen, textvariable=pass_room,show='*')
    pass_screen_entry.pack()
    Label(room_screen, text="").pack()
    Button(room_screen, text="OK", width=10, height=1, command = send_user).pack()

def main_lobby_screen():
    global main_lobby
    main_lobby = Tk()
    main_lobby.geometry("700x300")
    main_lobby.title(username1)
    Label(text="Chat App", width="200",height="2",font =("Calibri",13)).pack()
    messages_frame = Frame(main_lobby)
    online_clients = StringVar()
    online_clients.set("")
    scrollbar = Scrollbar(messages_frame)
    online_list = Listbox(messages_frame,height = 10,width = 40,yscrollcommand=scrollbar.set,fg="white",bg="black")
    scrollbar.pack(side=RIGHT,fill=Y)
    online_list.pack(side=LEFT,fill=BOTH)
    online_list.pack()
    msg = sock.recv(BUFSIZ).decode("utf8")
    online_list.insert(tkinter.END, msg)
    messages_frame.pack()
    Label(text="").pack()
    create_room_button = Button(main_lobby,text="create group chat",height="2", width="20",command=create_room,fg="white",bg="blue",activeforeground="red",activebackground="pink").pack(side = LEFT)
    check_user_button = Button(main_lobby,text="check user",height="2",width="20",command=check_user,fg="white",bg="blue",activeforeground="red",activebackground="pink").pack(side=RIGHT)
    online_user_button = Button(main_lobby,text="setup info",height="2",width="20",command=setup_info,fg="white",bg="blue",activeforeground="red",activebackground="pink").pack(side=RIGHT)
    change_password=Button(main_lobby,text="change password",height="2",width="20",command=changepass,fg="white",bg="blue",activeforeground="red",activebackground="pink").pack(side=RIGHT)
    lobby=Button(main_lobby,text="request room",height="2",width="20",command=wait,fg="white",bg="blue",activeforeground="red",activebackground="pink").pack(side=RIGHT)
    Label(text="").pack()
    main_lobby.mainloop()
def delete_entry():
    main_lobby.destroy()
main_account_screen()
main_lobby_screen()
sock.send(bytes(username1,'utf8'))
top = tkinter.Tk()
top.title("Phòng chat nhóm")
messages_frame = tkinter.Frame(top)

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=20, width=75, yscrollcommand=scrollbar.set,foreground="white",background="black")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

button_label = tkinter.Label(top, text="Enter Message:")
button_label.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg, foreground="black",background="white")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
Hello_button = tkinter.Button(top, text="Hello", command=Hello)
Hello_button.pack()
Bye_button = tkinter.Button(top, text="Goodbye", command=Goodbye)
Bye_button.pack()
Upload_button=tkinter.Button(top, text="Upload", command=Upload)
Upload_button.pack()
Download_button=tkinter.Button(top, text="Download", command=Download)
Download_button.pack()
quit_button = tkinter.Button(top, text="Quit", command=on_closing)
quit_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)




receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.