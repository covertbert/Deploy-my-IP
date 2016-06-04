import socket
import smtplib
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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


def check_stored_ip():
    with open('ip.txt', 'r') as data_file:
        data = data_file.read()
        stripped_data = data[1:-1]
        return stripped_data


def write_ip_to_file():
    with open('ip.txt', 'w') as outfile:
        json.dump(get_ip(), outfile)


def ip_compare():
    if check_stored_ip() != get_ip():
        print 'The IP has changed from ' + check_stored_ip() + ' to ' + get_ip() + ''
        send_email()
        print 'New IP as been sent to specified email'
        write_ip_to_file()
        print 'New IP has been written to text file for checking'
    else:
        print 'The IP hasn\'t changed'


scheduler = BlockingScheduler()
scheduler.add_job(ip_compare, 'interval', minutes=5)
scheduler.start()
