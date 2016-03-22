#!/usr/bin/env python

from jinja2 import Template
import sys, os, shutil, subprocess, time

#########################################################
# A python script to generate .ovpn files. The script   #
# reads in data from data/username & data/VPNAddress    #
# it then uses this data to generate the files.         #
# if a username is read in which does not have a        #
# corresponding key/cert pair the script will           #
# prompt the user to create them.                       #
#########################################################


def client_rev(name):
    path = os.path.dirname(os.path.realpath('client-rev.py'))
    print name

    if not os.path.exists(path + "/out/" + name):
        print "ERROR: " + name + " not found"
        sys.exit(1)
    else:
        shutil.copy("keys/client/"+ name + "/" + name + ".crt", "easyrsa/EasyRSA-3.0.1/pki/issued/" + name + ".crt")
        os.chdir(path + '/easyrsa/EasyRSA-3.0.1/')             # cd to easyrsa directory
        subprocess.call( [path + '/easyrsa/EasyRSA-3.0.1/easyrsa', 'revoke', name])
        subprocess.call( [path + '/easyrsa/EasyRSA-3.0.1/easyrsa', 'gen-crl'])
        os.chdir(path)
        shutil.copy("easyrsa/EasyRSA-3.0.1/pki/crl.pem", path + "/crl.pem")

    with open(path + "/easyrsa/EasyRSA-3.0.1/pki/index.txt") as f:
        for line in f:
            if line[0] == 'R':
                print line

    print ""
    print "crl.pem file must be copied to /etc/openvpn directory on VPN server"
if __name__ == '__main__':
    revname = raw_input('Enter username of client you wish to revoke: ')
    client_rev(revname)