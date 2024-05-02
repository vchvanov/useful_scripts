#!/usr/bin/python3

import sys
import telnetlib
import os
import time
import getpass

def type1(host, port, timeout, login, passwrd, outlet, choice):
    
    tn = telnetlib.Telnet(host, port, int(timeout))
    print(host)

    username = tn.read_until(b"Username: ")
    tn.write(login.encode('utf-8') + b"\r\n")
#    print(str(username))
    print('username success')

    password = tn.read_until(b"Password: ")
    tn.write(passwrd.encode('utf-8') + b"\r\n")
#    print(str(password))    
    print('password success')

    outlread = tn.read_until(b"Switched CDU: ")
    tn.write(choice.encode('utf-8') + b" " + outlet.encode('utf-8') + b"\r\n")
#    print(str(outlread))
    approve = tn.read_until(b"  Command successful")
    print(choice + ' ' + outlet + ' successfully !')
    
    approve = tn.read_until(b"Switched CDU: ")
    tn.write(b"exit\r\n")
    time.sleep(1)


def type2(host, port, timeout, login, passwrd, outlet, choice) :

    tn = telnetlib.Telnet(host, port, int(timeout))
    print(host)

    username = tn.read_until(b"Username: ")
    tn.write(login.encode('utf-8') + b"\r\n")
#    print(str(username))
    print('username success')

    password = tn.read_until(b"Password: ")
    tn.write(passwrd.encode('utf-8') + b"\r\n")
#    print(str(password))    
    print('password success')

    outlread = tn.read_until(b"Switched PDU: ")
    tn.write(choice.encode('utf-8') + b" " + outlet.encode('utf-8') + b"\r\n")
#    print(str(outlread))
    approve = tn.read_until(b"  Command successful")
    print(choice + ' ' + outlet + ' successfully !')

    approve = tn.read_until(b"Switched PDU: ")
    tn.write(b"exit\r\n")
    time.sleep(1)

def type3(host, port, timeout, login, passwrd, outlet, choice):

    tn = telnetlib.Telnet(host, port, int(timeout))
    print(host)

    username = tn.read_until(b"User Name : ")
    tn.write(login.encode('utf-8') + b"\r\n")
#    print(str(username))
    print('username success')

    password = tn.read_until(b"Password  : ")
    tn.write(passwrd.encode('utf-8') + b"\r\n")
#    print(str(password))    
    print('password success')

    outlread = tn.read_until(b"apc>")
    tn.write(b"ol" + choice.encode('utf-8') + b" " + outlet.encode('utf-8') + b"\r\n")
#    print(str(outlread))
    approve = tn.read_until(b"E000: Success")
    print(choice + ' ' + outlet + ' successfully !')

    approve = tn.read_until(b"apc>")
    tn.write(b"exit\r\n")
    time.sleep(1)

def type4(host, port, timeout, login, passwrd, outlet, choice):

    tn = telnetlib.Telnet(host, port, int(timeout))
    print(host)

    username = tn.read_until(b"Username: ")
    tn.write(login.encode('utf-8') + b"\r\n")
#    print(str(username))
    print('username success')

    password = tn.read_until(b"Password: ")
    tn.write(passwrd.encode('utf-8') + b"\r\n")
#    print(str(password))    
    print('password success')
    
    if choice == "on" or choice == "off" :
        outlread = tn.read_until(b"# ")
        tn.write(b"power outlets " + outlet.encode('utf-8') + b" " + choice.encode('utf-8') + b"\r\n")
        tn.read_until(b"Do you wish to turn outlet " + outlet.encode('utf-8') + b" " + choice.encode('utf-8') + b"? [y/n] ")
        tn.write(b"y\r\n")
#        print(str(outlread))
        approve = tn.read_until(b"# ")
        print(choice + ' ' + outlet + ' successfully !')

        tn.write(b"exit\r\n")
        time.sleep(1)
    else :
        outlread = tn.read_until(b"# ")
        tn.write(b"power outlets " + outlet.encode('utf-8') + b" cycle" + b"\r\n")
        tn.read_until(b"Do you wish to cycle outlet " + outlet.encode('utf-8') + b"? [y/n] ")
        tn.write(b"y\r\n")
#        print(str(outlread))
        approve = tn.read_until(b"# ")
        print(choice + ' ' + outlet + ' successfully !')

        tn.write(b"exit\r\n")
        time.sleep(1)

def type5(host, port, timeout, login, passwrd, outlet, choice):

    tn = telnetlib.Telnet(host, port, int(timeout))
    print(host)

    username = tn.read_until(b"Username: ")
    tn.write(login.encode('utf-8') + b"\r\n")
#    print(str(username))
    print('username success')

    password = tn.read_until(b"Password: ")
    tn.write(passwrd.encode('utf-8') + b"\r\n")
#    print(str(password))    
    print('password success')

    if choice == "on" or choice == "off" :
        outlread = tn.read_until(b"> ")
        tn.write(b"power outlets " + outlet.encode('utf-8') + b" " + choice.encode('utf-8') + b"\r\n")
        tn.read_until(b"Do you wish to turn outlet " + outlet.encode('utf-8') + b" " + choice.encode('utf-8') + b"? [y/n] ")
        tn.write(b"y\r\n")
#        print(str(outlread))
        approve = tn.read_until(b"> ")
        print(choice + ' ' + outlet + ' successfully !')

        tn.write(b"exit\r\n")
        time.sleep(1)
    else :
        outlread = tn.read_until(b"> ")
        tn.write(b"power outlets " + outlet.encode('utf-8') + b" cycle" + b"\r\n")
        tn.read_until(b"Do you wish to cycle outlet " + outlet.encode('utf-8') + b"? [y/n] ")
        tn.write(b"y\r\n")
#        print(str(outlread))
        approve = tn.read_until(b"> ")
        print(choice + ' ' + outlet + ' successfully !')

        tn.write(b"exit\r\n")
        time.sleep(1)
