import os
import subprocess

#subprocess.call(['chmod', '0777', '/etc/squid/squid.conf'])
def add_port(username,port_num):
	file = open('/etc/squid/port.conf','a') 
	file.write("\n"+"acl Safe_ports port "+str(port_num))
	file.close()
	subprocess.call('sudo systemctl reload squid.service',shell=True)


def add_mac(username,mac):
	file = open('/etc/squid/config_files/'+username+'/'+username+'_mac.lst','a') 
	file.write("\n"+str(mac))
	file.close()
	subprocess.call('sudo systemctl reload squid.service',shell=True)


def add_website(username,website):
	file = open('/etc/squid/config_files/'+username+'/'+username+'_website.lst','a') 
	file.write("\n"+str(website))
	file.close()
	subprocess.call('sudo systemctl reload squid.service',shell=True)

def remove_mac(username,mac):
	file = open('/etc/squid/config_files/'+username+'/'+username+'_mac.lst','r')
	macsList = file.readlines()
	file.close()
	file = open('/etc/squid/config_files/'+username+'/'+username+'_mac.lst','w')
	file.close()
	for line in macsList: 
		file = open('/etc/squid/config_files/'+username+'/'+username+'_mac.lst','a')
		if str(line.strip())!=mac and line.strip()!="":
			file.write("\n"+str(line.strip()))		
		file.close()
	subprocess.call('sudo systemctl reload squid.service',shell=True)

def remove_port(username,port):
	file = open('/etc/squid/port.conf','r')
	portsList = file.readlines()
	file.close()
	file = open('/etc/squid/port.conf','w')
	file.close()
	for line in portsList: 
		file = open('/etc/squid/port.conf','a')
		if str(line.strip())!=("acl Safe_ports port "+str(port)) and line.strip()!="":
			file.write("\n"+str(line.strip()))		
		file.close()
	subprocess.call('sudo systemctl reload squid.service',shell=True)

def remove_website(username,website):
	file = open('/etc/squid/config_files/'+username+'/'+username+'_website.lst','r')
	websitesList = file.readlines()
	file.close()
	file = open('/etc/squid/config_files/'+username+'/'+username+'_website.lst','w')
	file.close()
	for line in websitesList: 
		file = open('/etc/squid/config_files/'+username+'/'+username+'_website.lst','a')
		if str(line.strip())!=website and line.strip()!="":
			file.write("\n"+str(line.strip()))		
		file.close()
	subprocess.call('sudo systemctl reload squid.service',shell=True)
