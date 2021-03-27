#!/usr/bin/python3
import argparse
import subprocess #to do most of the heavy lifting for masscan and nmap, as I don't like the python modules for Masscan and Nmap

#Usage
parser = argparse.ArgumentParser(description="Usage example: \033[1;35;40msudo python3 masscan_to_nmap.py -i 10.10.10.11\033[0;37;40m")
parser.add_argument("-i", "--ip", help="Input an IP address to scan", required=True)
parser.add_argument("-n", "--network", help="Network to listen on, such as eth0, tun0 etc. Default is tun0, if you give no option", required=False, default='tun0')
args = parser.parse_args()
print ("\nRunning \033[1;32;40mMasscan\033[0;37;40m on network\033[1;32;40m " + args.network + "\033[0;37;40m against the IP \033[1;32;40m" + args.ip + "\033[0;37;40m to quickly identify open ports\n")                                                                                                      
                                                                                                                                                       
#Masscan                                                                                                                                               
masscan_cmd = ('sudo masscan -p1-65535,U:1-65535 ' + args.ip + ' --rate=1000 -e ' + args.network + ' > masscan.txt' ) # it will output results to masscan.txt. This self deletes later, I just don't have a clever way to grep the port results from masscan to use in nmap                                    
subprocess.check_call(masscan_cmd, shell=True) #.check_call stops the entire masscan command from showing. To show command, change to subprocess.call().                                                                                                                                                      
                                                                                                                                                       
#grep and filter ports from Masscan output and feed into Nmap scan                                                                                     
grep_cmd = ("awk '{print $4}' masscan.txt | cut -d '/' -f 1 | awk -F/ '{print$1}' ORS=',' ")                                                           
grepped_ports = subprocess.run(grep_cmd, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)                                      
ports = grepped_ports.stdout                                                                                                                           
                                                                                                                                                       
#Nmap scan, and output results to a txt file                                                                                                           
nmap_cmd = ("sudo nmap " + args.ip + " -T4 -A -Pn -p " + ports + " > nmap_" + args.ip + ".txt")                                                        
print ("\nRunning Nmap scan against \033[1;32;40m" + args.ip + "\033[0;37;40m with the following ports \033[1;32;40m" + ports + "\033[0;37;40m \n")                                                                                                                                                  
subprocess.call(nmap_cmd, shell=True)                                                                                                                  
                                                                                                                                                       
#delete masscan.txt now it's served its grep purpose                                                                                                   
subprocess.run(['rm masscan.txt'], shell=True)

#print nmap results
print ('\nNmap results saved to \033[1;35;40mnmap_' + args.ip + '.txt \033[0;37;40m \n')
f = open('nmap_' + args.ip + '.txt', 'r')
print (f.read())
