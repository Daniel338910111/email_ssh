import smtplib
import threading
import time
import os
import platform
import pyautogui

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

try:
    import easyimap
except:
    print('please install "easyimap"\ncommand: "pip install easyimap"\nand then run this script')
    time.sleep(20)
    exit()
    


class email_ssh: # a very original name
    def __init__(self, email, google_username, password):
        self._email = email
        self._password = password
        self._username = google_username
        self.image = None
        self._message = MIMEMultipart()

    def screenshot(self):
        """
        taking a screen shot of the main monitor
        sending it and then deleting it from your pc
        to save space
        """
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshots/screenshot.png')
        image = open('screenshots/screenshot.png', 'rb').read()
        self.image = MIMEImage(image, name='Took now')
        return self._message.attach(self.image)

    def shutdown_program(self):
        """closing the program via command q"""
        exit()

    def shutdown_pc(self):
        """Shutting down the pc via command shutdown"""
        if platform.lower() == 'windows':
            os.system('shutdown -s')
        else:
            os.system('shutdown -h +1 "Shutting down via Email command"')
        exit()
        
    def send_by_command(self, command):
        """
        getting the command and sending a message according to
        the given command
        """
        
        server = smtplib.SMTP('smtp.gmail.com', 587) # google smtp server
        server.starttls()
        server.login(self._email, self._password) 
        # login to google with the given args
        
        self._message['From'] = self._email
        self._message['To'] = self._email # sending to yourself
        self._message['Subject'] = 'Pyspy' # do not change
        # you can run more then one script by adding an ID to the subject
        # like self._message['Subject'] = 'Pyspy1' and so on
        
        print('The command I got ' +str(command.lower()))
        
        
        commands_functions={'screenshot': self.screenshot,
                            'shutdown': self.shutdown_pc(),
                            'q': self.shutdown_program,
                            }

        commands_functions.get(command.lower(), self._message.attach(MIMEText(
                                                'command not found', 'plain'
                                                )))() # call the function at the end

        text = self._message.as_string() # converting the messages to a string
        server.sendmail('Pyspy', self._email, text)
        server.quit()
        print('email sended...')
        try:
            os.remove('screenshots/screenshot.png')
        except:
            pass
        
    def run(self):
        """
        checking your email every 20s
        """
        reciver = easyimap.connect('imap.gmail.com', self._email, self._password)
        checked_emails = [] # to not make the last given command
        # all the checked commands going to here
        
        while True:
            for gmail in reciver.listids(limit=1): # checking the last email
                
                mail = reciver.mail(gmail) # getting the email ID
                print(gmail)
                print('checking ' +str(mail.title) +' From ' +mail.from_addr)
                
                if mail.from_addr == '"{0._username}" <{0._email}>'.format(self):
                    if mail.title != 'Pyspy':
                        print('Got a command!\nsending mail...')
                        command = mail.body
                        self.send_by_command(command.strip()) # IDK if I don't take the spaces off
                        # it wont recognize the given command that is why
                        # whem making a command it must be only 1 arg like "test"
                        
                        checked_emails.append(gmail) # adding to check emails
                        # to not repeat the comman 
                    else:
                        print('passing...\n') # if the command is not from you email
                        
                print('\nchecked\n')
                time.sleep(20) # to not spam the internet
            


if __name__=='__main__':
    print('I recommand running this script on .pyw\n')
    activate = email_ssh(email='your@gmail.com', # you gmail
                         google_username='yourUserName', # your google username
                         password='yourPassword123' # your google password
                         )
    
    try:
        activate.run()
    except Exception as e:
        print('Error: ' +str(e) +'\n\n')
        print('please read the ERROR\nThere are 3 possibilities why this happend:\n'
              '1. the given email//username//password are wrong\n'
              '2. you didn\'t allowed low level security apps connect to your email\n'
              '3. you are connected from too many devices (google allows only 15)\n'
              'Please check this from 1 to 3 as presented\n\n'
              'shutting down in more 40s')
        time.sleep(40)
        exit()
         
    
