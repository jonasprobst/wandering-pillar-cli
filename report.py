#Report.py
#Report the current state a wandering pillar to a restfull web database.

#todo:
#- add debugging option (verbose... -v ?)

import argparse, json, requests, datetime, logging, sys

#setup logging
logging.basicConfig(filename="wapi.log", level=logging.DEBUG)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.info("\n\n>> REPORT:PY - {0}".format(now))

#hack to disable security warning. CHeck the follwoing docs. i know it's not pretty...
#https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
logging.captureWarnings(True)

parser = argparse.ArgumentParser(description="report state of wandering-pillar to restfull database.", version="0.1")
parser.add_argument("id", type=int, help="device id")
parser.add_argument("-u", "--baseurl", default="https://wapi.firebaseio.com", dest="baseurl", help="firebase baseurl.")
parser.add_argument("-l", "--motorLft", type=int, dest="motorLeft", nargs=6, help="left motor values: [rpm, current, stop, enable, direction, gear]")
parser.add_argument("-r", "--motorRgt", type=int, dest="motorRight", nargs=6, help="right motor values: [rpm, current, stop, enable, direction, gear]")
parser.add_argument("-b", "--battery", type=int, dest="batteryLevel", help="batery level")
parser.add_argument("-s", "--step", type=int, help="step number")
parser.add_argument("-t", "--timer", type=int, help="timer value")
args = parser.parse_args()

#build json data
data = {}
data['timestamp'] = now
data['batteryLevel'] = args.batteryLevel
data['autoStep'] = args.step
data['autoTimer'] = args.timer

if args.motorLeft:
    motorLeft = {}
    motorLeft['rpm'] = args.motorLeft[0]
    motorLeft['current'] = args.motorLeft[1]
    motorLeft['stop'] = args.motorLeft[2]
    motorLeft['enable'] = args.motorLeft[3]
    motorLeft['direction'] = args.motorLeft[4]
    motorLeft['gear'] = args.motorLeft[5]
    data['motorLeft'] = motorLeft


if args.motorRight:
    motorRight = {}
    motorRight['rpm'] = args.motorRight[0]
    motorRight['current'] = args.motorRight[1]
    motorRight['stop'] = args.motorRight[2]
    motorRight['enable'] = args.motorRight[3]
    motorRight['direction'] = args.motorRight[4]
    motorRight['gear'] = args.motorRight[5]
    data['motorRight'] = motorRight

#upload to db, catch all errors
try:
    url = args.baseurl + "/devices/{0}/data.json".format(args.id)
    r = requests.post(url, json=data)
    if not r.status_code == 200:
        logging.debug("status_code: {0}, body: {1}".format(r.status_code, r.text))

except Exception as e:
    logging.debug("Error: {0}".format(e))

sys.exit(1)

#r.json(), r.text,
#r = requests.post() -> add to a list of data
#r = requests.get()
#r = requests.put() -> write or replace
#r = requests.delete()
