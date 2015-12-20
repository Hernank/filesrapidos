# telnet program example
import telnetlib
import time

user='admin'
password='admin'
host='localhost'

try:
    tn=telnetlib.Telnet(host,8000)
    tn.read_until(b"Login: ")
    tn.write(user.encode() + "\r\n".encode())
    tn.read_until(b"Password: ")
    tn.write(password.encode() + "\r\n".encode())
    print("Connection establised")
except Exception:
    print("Connection failed")

cmd="interface AccessPoint\r\n"
tn.write(cmd.encode())
cmd2="ssid TEST\r\n"
tn.write(cmd2.encode())

output=n.read_eager()
while output:
    print(output.decode())
    time.sleep(.2)
    output=tn.read_eager()