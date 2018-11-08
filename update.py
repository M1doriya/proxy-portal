import os
import subprocess

#subprocess.call(['chmod', '0777', '/etc/squid/squid.conf'])
def update_port(port_num):
	file = open('/etc/squid/squid.conf','a') 
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





# squid.conf to temp.txt
'''file2 = open('temp.txt','w') 
file = open('/etc/squid/squid.conf', 'r')
data = file.readlines() 
for line in data: 
	#if(line[0]!="#" and line!="" and line!="\n"):
		file2.write(line)
file.close()
file2.close()'''

# temp.txt to squid.conf
'''file2 = open('/etc/squid/squid.conf','w') 
file = open('temp.txt', 'r')
data = file.readlines() 
for line in data: 
	#if(line[0]!="#" and line!="" and line!="\n"):
	file2.write(line)
file.close()
file2.close()'''
