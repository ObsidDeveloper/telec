import sys
import socket
import re
import threading
import os

#regs
template = r'\d{4}\s[0-9A-Fa-f][0-9A-Fa-f]\s\d{2}[:][0-5][0-9][:][0-5][0-9][.]\d{3}\s\d{2}'

log_file = open("log.txt", "w")


def line_parse(line):
    parsed = re.split(r'[\s.:]', line)
    if parsed[6] == "00":
        dec = parsed[5][0]
        output_str = "Спортсмен, нагрудный номер {0}, прошел отсечку {1} в {2}:{3}:{4}".format(parsed[0], parsed[1], parsed[2], parsed[3], dec)
        print(output_str)
        log_file.write(output_str + "\n")
    else:
        log_file.write(line + "\n")

def process_reques(conn, client_address):
    
    try:
        while True:
            data = conn.recv(60)
            line = data.decode("utf-8").split("\r\n", 1)[0]
            
            if line == "shutdown":
                log_file.close()
                conn.close()
                os.abort()
            if line == "exit":
                return
                
            if re.match(template, line) is not None:
                line_parse(line)
            else:
                print("Wrong format")
    finally:
        conn.close()
        
def serv_start(host, port):
    print(f'Run port {port}')
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(0)
    log_file.write(f'Run port {port}\n')

    try:
        while True:
            conn, client_address = sock.accept()
            thread1 = threading.Thread(target = process_reques, args = (conn, client_address))
            #process_reques(conn, client_address)
            thread1.start()
    finally:
        sock.close()
        log_file.close()
    
if __name__ == '__main__':
    print("start")
    serv_start('localhost', 8080)