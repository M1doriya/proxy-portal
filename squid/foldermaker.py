import os
name="icm2016006@iiita.ac.in"
filename = "config_files/"+name[:-12]+"/"+name[:-12]+"_squid.conf"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(" ")
filename = "config_files/"+name[:-12]+"/"+name[:-12]+"_mac.txt"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(" ")