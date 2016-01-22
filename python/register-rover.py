import requests
import json
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]

while (True):
	payload = {'name': 'Chipy', 'classroom': 'Mr. Hurlburt', 'ip_addr': ip}
	r = requests.post("http://ec2-52-3-242-191.compute-1.amazonaws.com/register-rover.php", data=payload)
	time.sleep(2)


socket.close();
