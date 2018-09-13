import os
import subprocess

#subprocess.call(['chmod', '0777', '/etc/squid/squid.conf'])
def update_port(port_num):
	file = open('/etc/squid/squid.conf','w') 
	file.write("\n"+"acl              "+str(port_num))
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
