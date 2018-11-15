import os
import subprocess

#subprocess.call(['chmod', '0777', '/etc/squid/squid.conf'])
def update_port(username,port_num):
	file = open('/etc/squid/config_files/'+username+'/'+username+'_squid.conf','a') 
	file.write("\n"+"acl Safe_ports port "+str(port_num))
	file.write("\n"+"http_access deny !Safe_ports")
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