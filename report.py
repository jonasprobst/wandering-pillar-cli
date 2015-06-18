#http://ozgur.github.io/python-firebase/

import argparse, json
from firebase import firebase
#from firebase import jsonutil

parser = argparse.ArgumentParser(description="report state of wandering-pillar to restfull database.", version="0.1")
parser.add_argument("did", type=int, help="device id")
parser.add_argument("-l", "--motorLft", type=int, dest="motorLft", nargs=6, help="left motor values: [rpm, current, stop, enable, direction, gear]")
parser.add_argument("-r", "--motorRgt", type=int, dest="motorRgt", nargs=6, help="right motor values: [rpm, current, stop, enable, direction, gear]")
parser.add_argument("-b", "--battery", type=int, dest="batteryLevel", help="batery level")

args = parser.parse_args()

print "Device id:", args.did
print "Battery Level:", args.batteryLevel
print "Left motor values [rpm, current, stop, enable, direction, gear]", args.motorLft
print "Right motor values [rpm, current, stop, enable, direction, gear]", args.motorRgt

#build json object

#connect to firebase (authenticate?!)
firebase = firebase.FirebaseApplication('https://wapi.firebaseio.com', None)

#get
#result = firebase.get('/devices', None)
#print result

#post
new_data = args.did
result = firebase.post('/devices/', new_data, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print result

#put ??

#delete
#firebase.delete('/users', '1')
