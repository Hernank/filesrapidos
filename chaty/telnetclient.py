import getpass
import sys
import telnetlib

HOST = "localhost"
user = raw_input("Usuario: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST,8000)

tn.read_until("Username: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")

tn.write("show ver | include IOS\n")
tn.write("exit\n")

print tn.read_all()
