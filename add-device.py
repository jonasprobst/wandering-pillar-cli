import argparse, json, requests

parser = argparse.ArgumentParser(description="create a new wandering pillar device on firebase.", version="0.1")
parser.add_argument("-u", "--baseurl", default="https://wapi.firebaseio.com", dest="baseurl", help="firebase baseurl.")
parser.add_argument("-n", "--name", dest="deviceName", help="device name")
parser.add_argument("-l", "--location", dest"deviceLocation", help="device location")
args = parser.parse_args()

#edit device device data here
data = {}
data['name'] = 'Wandering Pillar'
data['location'] = 'Centre PasquArt, Biel'
data['mode'] = 'manual'
data['cmd'] = 'stop'
data['data'] = {}
data['program'] = {}

#make device id > number of devices
url = baseurl, "/devices"
print url
r = requests.get(url)
print r.text

#get id of last element
#new id the last id + 1
did = 2


url = "https://wapi.firebaseio.com/devices/%s.json" % did
r = requests.put(url, json=data)

#if all went well return new did
print r.text
