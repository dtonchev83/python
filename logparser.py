#Created by Dobromir Tonchev on 27 Aug 2020
#Task description:
#Please write a script in python or bash to parse a standard Linux /var/log/messages (or syslog) log 
#file and search for any IP addresses.
#For each unique IP address, the script should output the IP address, it’s hostname (if resolvable), the time of the log, and if it is still active on the network.
#End of task description.


#using python 3.8, script will match ipv4 addresses only.


import argparse
import re
import socket
import subprocess


#usage function - shows usage as well as selecting file that will be parsed
parser = argparse.ArgumentParser(description='search for all ipv4 format IPs in a specified file')
parser.add_argument('filename', help='full path and name of the file that you want to check')
args = parser.parse_args()
filename = args.filename

#two dictionaries that will be used during execution
ip_dict=dict()
all_ips={}


    
#main function - parse a file, call two functions - pingIP that is used to tell
#whether IP is active(replies to ping) and resolveIP that is used to tell if IP address resolves to hostname
#in dns and /etc/hosts
def main(filename):
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    with open(filename,'r') as file:
        for line in file:
            if pattern.findall(line):   
                for a in pattern.findall(line):
                    timestamp = (' ' .join(line.split()[0:3]))
                    if a not in ip_dict and not a.startswith('0'):
                        ip_dict[a]={}
                        ip_dict[a]['IP'] = (timestamp)
                    elif a in ip_dict:
                        timestamp_list = (ip_dict[a]['IP'])
                        timestamp_list = ((''.join(timestamp_list)) + ' ' +  timestamp)
                        ip_dict[a]['IP'] = timestamp_list
       

    for key in ip_dict.keys():
        pingIP(key)
        fqdn = resolveIP(key)
        if fqdn != (None):
            ip_dict[key]['FQDN']=fqdn[0]
        elif fqdn == None:
            ip_dict[key]['FQDN']='Nothing'
        #in case one ping at a time is executed, below line is uncommented
        #print(key + ' appeared on ' + ip_dict[key]['IP'] + ', is IP active - ' + ip_dict[key]['Active'] + ', resolves to ' + ip_dict[key]['FQDN'] )
    
    
    while all_ips:
        for key, proc in list(all_ips.items()):
            if proc.poll() is not None:
                del all_ips[key]
                if proc.returncode == 0:
                    ip_dict[key]['Active']='Yes'
                else:
                    ip_dict[key]['Active']='No'
    
    for key in ip_dict.keys():
        print(key + ' appeared on ' + ip_dict[key]['IP'] + ', is IP active - ' + ip_dict[key]['Active'] + ', resolves to ' + ip_dict[key]['FQDN'] )

def resolveIP(key):
    try:
        return socket.gethostbyaddr(key)  
    except socket.herror:
        return None

# run all pings in paralel
def pingIP(key):
    command = ['ping', '-c', '1', '{}'.format(key)]
    all_ips[key]=subprocess.Popen(command, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

# run each ping one at a time
# #def pingIP(key):
#    command = ['ping', '-c', '1', '{}'.format(key)]
#    alive=(subprocess.call(command, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))


#    if alive == 0:
#        print(key + ' active')
#        ip_dict[key]['Active']='Yes'
#    else:
#        print(key + ' not active')
#        ip_dict[key]['Active']='No'

main(filename)