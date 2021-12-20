import socket,re, os
PORT = 90
from pathlib import Path
HOST = 'localhost'
curr_dir = "\\"
sock = ''
MAIN_DIR = Path(os.getcwd(), 'users')

def msg_user(login, password, curr_dir, msg, c = 0):
    return f"{login}=login, {password}=password, {curr_dir}=curr_dir, {c}=len, {msg}=message".encode()

def to(login, password, curr_dir, req):
    global sock
    name = re.split("[ \\/]+", req)[-1]
    curr_path_file = Path(MAIN_DIR, name)
    sock.send(f'send {name}'.encode())
    with open(curr_path_file, 'r') as file:
        text = file.read()
    print(text.encode())
    sock.send(msg_user(login, password, curr_dir, text.encode(), len(text)))
    return


def result(req):
    global sock, f1, f2, MAIN_DIR, curr_dir
    flag_finder = sock.recv(1024)
    name = re.split("[ \\/]+", req)[-1]
    print(name)
    length = sock.recv(1024).decode()
    text = sock.recv(len(length)).decode()
    curr_path_file = Path(MAIN_DIR, name)
    with open(curr_path_file, 'w') as file:
        file.write(text)
    return

def main():
    global sock
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    curr_dir = login
    print(f"Присоединились к {HOST} {PORT}")
    while True:
        req = input(curr_dir+'$ ')
        req = req.strip()
        if req == 'exit':
            break
        sock = socket.socket()
        sock.connect((HOST, PORT))
        if req.find("send_from") == 0:
            if req == "send_":
                print("Нет файла")
            else:
                to(login, password, curr_dir, req)

        else:
            sock.send(msg_user(login, password, curr_dir, req))
            if req.find("get_to") == 0 or req == "get_to":
                result(req)
            else:

                response = sock.recv(1024).decode()
                if req.find("cd") == 0:
                    if ".." in req:
                        curr_dir = login
                    else:
                        curr_dir = response[response.find("\\", response.find(login)):]
                else:
                    print(response)
                    
if __name__ == '__main__':
    main()