import socket
import smtplib
import json

from pprint import pprint
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler


# Get password
def get_password():
    with open('password.json') as data_file:
        data = json.load(data_file)
        return data['password']


# Get IP
def get_ip():
    ip_address = ([l for l in (
        [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
            [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
             [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    return ip_address


# Send email
def send_email():
    fromaddr = "deployddetails@gmail.com"
    toaddr = "blackmanrgh@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your IP"

    body = get_ip()
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, get_password())
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Send email every 4 hours
scheduler = BlockingScheduler()
scheduler.add_job(send_email, 'interval', hours=24)
scheduler.start()
