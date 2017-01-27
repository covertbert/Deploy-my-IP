import socket
import smtplib
import json
import subprocess
import logging

from bs4 import BeautifulSoup, Tag
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig()


# Get IP
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


# Write textfile to HTML
def write_html():
    soup = BeautifulSoup(open('dist/index.html'), 'html.parser')
    ip = soup.findAll('h1', { 'class' : 'ip-address' })[0].string
    ip.replaceWith(get_ip())
    html = soup.prettify('utf-8')
    with open('dist/index.html', 'wb') as file:
        file.write(html)


# Send email with all the stuff
def deploy_ip():
    bashCommand = 'firebase deploy'
    subprocess.check_output(['bash','-c', bashCommand])


# Checks the IP stored in ip.txt and returns it
def check_stored_ip():
    with open('dist/ip.txt', 'r') as data_file:
        data = data_file.read()
        stripped_data = data[1:-1]
        return stripped_data


# Writes the IP to ip.txt
def write_ip_to_file():
    with open('dist/ip.txt', 'w') as outfile:
        json.dump(get_ip(), outfile)


# Compares the current IP with that from the txt file. If it hasn't changed it does nothing. If it has then it sends
# the email and writes the new IP to the txt file
def ip_compare():
    if check_stored_ip() != get_ip():
        print 'The IP has changed' 
        write_ip_to_file()
        print 'New IP has been written to text file for checking'
        write_html()
        print 'New IP has been written to HTML file for deployment'
        deploy_ip()
    else:
        print 'The IP hasn\'t changed'

# Writes initial IP to text file when the script starts just in case the txt file doesn't already exist.
write_ip_to_file()

# Runs the ip_compare function every 5 minutes
scheduler = BlockingScheduler()
scheduler.add_job(ip_compare, 'interval', minutes=1)
scheduler.start()
