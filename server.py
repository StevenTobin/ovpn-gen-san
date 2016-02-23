#!/usr/bin/env python

import os, subprocess, time, shutil

##################################################
# A python script to generate server key pairs.  #
# The script reads in data from data/VPNAddress  #
##################################################

def server_gen():

	path = os.path.dirname(os.path.realpath('server.py')) 

	vpn_addr = {}
	with open("data/VPNAddress") as f:
		for line in f:
			(add, grid) = line.split()
			vpn_addr[grid] = add

	
	for grid, add in vpn_addr.items():
		if not os.path.exists("keys/server/" + grid +""):
			os.makedirs("keys/server/" + grid +"-noc-vpn1")
    		os.chdir(path + '/easyrsa/EasyRSA-3.0.1/')               # cd to easyrsa directory
    		keygen = subprocess.Popen( path + '/easyrsa/EasyRSA-3.0.1/easyrsa build-server-full '+ grid + ' nopass', shell = True, stdout=subprocess.PIPE)
    		keygen.wait()
       	 	print keygen.returncode
       	 	os.chdir(path)
        	time.sleep(3)     # Wait a bit for key pair to be created before moving, juuuuust in case
        	shutil.move("easyrsa/EasyRSA-3.0.1/pki/private/" + grid + ".key", "keys/server/"+ grid +"/" + grid + ".key" )
        	shutil.move("easyrsa/EasyRSA-3.0.1/pki/issued/" + grid + ".crt", "keys/server/" + grid + "/" + grid + ".crt")
        	print "##########################################################"
       		print ' Key/Cert pair generated for: '+ grid +"-noc-vpn1 "
        	print "##########################################################"


if __name__ == '__main__':
	server_gen()