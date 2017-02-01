""" This script checks for local IP changes and deploys them to firebase """

import socket
import json
import subprocess
import logging

from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig()


def get_ip():
    """ Gets the current IP address """
    the_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    the_socket.connect(('8.8.8.8', 80))
    return the_socket.getsockname()[0]


def write_html():
    """ Writes the IP from text file to the HTML file for deployment """
    soup = BeautifulSoup(open('dist/index.html'), 'html.parser')
    ip_address = soup.findAll('h1', {'class' : 'ip-address'})[0].string
    ip_address.replaceWith(get_ip())
    html = soup.prettify('utf-8')
    with open('dist/index.html', 'wb') as index_file:
        index_file.write(html)


def deploy_ip():
    """ Deploys the dist folder containing the updated IP address etc """
    bash_command = 'firebase deploy'
    subprocess.check_output(['bash', '-c', bash_command])


def check_stored_ip():
    """ Checks the IP stored in ip.txt and returns it """
    with open('dist/ip.txt', 'r') as data_file:
        data = data_file.read()
        stripped_data = data[1:-1]
        return stripped_data


def write_ip_to_file():
    """ Writes the IP to ip.txt """
    with open('dist/ip.txt', 'w') as outfile:
        json.dump(get_ip(), outfile)


def ip_compare():
    """ Compares IP with that from text file. If change - deploy, else nothing """
    if check_stored_ip() != get_ip():
        print 'The IP has changed'
        write_ip_to_file()
        print 'New IP has been written to text file for checking'
        write_html()
        print 'New IP has been written to HTML file for deployment'
        deploy_ip()
    else:
        print 'The IP hasn\'t changed'


# Runs the ip_compare function every 5 minutes
SCHEDULER = BlockingScheduler()
SCHEDULER.add_job(ip_compare, 'interval', minutes=1)
SCHEDULER.start()
