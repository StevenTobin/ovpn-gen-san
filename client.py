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


def client_gen():

# Read in the list of IP addresses and grid names
# vpn_addr = dict, grid = gridname, add = server address
    vpn_addr = {}
    with open("data/VPNAddress") as f:
        for line in f:
            (add, grid) = line.split()
            vpn_addr[grid] = add

# Read in the list of usernames
    usrnames = open("data/username", "r")
    names = usrnames.read().split(',')
    names[-1] = names[-1].strip()        # Get rid of the new line character

# Iterate through each username adding the user keys and
# the tls auth key and inserting the correct ip address 
# for each server, then output the file with the username
# and correct gridname <username>@<gridname>

    for n in names:
        for grid, add in vpn_addr.items():
            username = n
            if not os.path.exists("out/" +username):
                os.makedirs("out/" + username)
                os.makedirs("out/" + username + "/"+ username)

            ca = 'keys/ca.crt'
            if os.path.isfile(ca) == False:
                print 'Error: ca.crt not found!'
                print ' The ca.crt file should be in the keys directory'
                sys.exit(1)

            usercert = 'keys/client/' + username +'/' + username +'.crt'
            if os.path.isfile(usercert) == False:
                print username + '.crt not found'
                choice = ''
                while choice not in ['y', 'n']:
                    choice = raw_input('Create new key and certificate for '+ username +' (y/n)?')
                    if choice == 'y':
                        path = os.path.dirname(os.path.realpath('client.py'))  # Find the location of the script
                        os.chdir(path + '/easyrsa/EasyRSA-3.0.1/')             # cd to easyrsa directory
                        keygen = subprocess.Popen( path + '/easyrsa/EasyRSA-3.0.1/easyrsa build-client-full '+ username + ' nopass', shell = True, stdout=subprocess.PIPE) # Generate the <username> key
                        keygen.wait()
                        os.chdir(path)
                        time.sleep(3)     # Wait a bit for key pair to be created before moving, juuuuust in case
                        os.makedirs("keys/client/"+ username)
                        shutil.move("easyrsa/EasyRSA-3.0.1/pki/private/" + username + ".key", "keys/client/"+ username +"/"+ username +".key" )
                        shutil.move("easyrsa/EasyRSA-3.0.1/pki/issued/" + username + ".crt", "keys/client/"+ username + "/" + username + ".crt")
                        usercert = 'keys/client/' + username +'/' + username +'.crt'
                    else:
                        print "Error: " + username + ".crt not found"
                        print 'The '+ username + '.crt file should be in the keys/'+ username +' directory'

            userkey = 'keys/client/' + username + '/' + username +'.key'
            if os.path.isfile(userkey) == 'False':
                print 'Error: ' +username + '.key not found'
                sys.exit(1)

            tlsauthcert = 'keys/ta.key'
            if os.path.isfile(tlsauthcert) == False:
                print 'Error: tls.key not found'
                sys.exit(1)

            userovpn = username +"@" + grid + '.ovpn'

            # Assemble the .ovpn file and output
            with open('data/ovpn.template') as ovpntemplate, \
                open(usercert) as certfile, \
                open(userkey) as keyfile, \
                open(ca) as cafile, \
                open(tlsauthcert) as tlsauthfile, \
                open(userovpn, 'w') as outfile:
                model = Template(ovpntemplate.read())
                addressvalue = add
                certvalue = certfile.read()
                keyvalue = keyfile.read()
                cavalue = cafile.read()
                tlsauthvalue = tlsauthfile.read()
                outfile.write(model.render(usercert=certvalue, userkey=keyvalue, cacert=cavalue, address=addressvalue, tlsauth=tlsauthvalue))
                shutil.move( username +"@" + grid + '.ovpn', "out/" + username +"/" + username +"/" + username + "@" + grid + '.ovpn')
                print 'OVPN file generated: ' + username +"@" + grid + '.ovpn'
                
                
            shutil.make_archive('out/'+ username, 'zip', "out/" + username)

        print ''

    print '*'*30
    print ''

if __name__ == '__main__':
    client_gen()