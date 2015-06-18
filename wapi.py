#prerequisites:
# $ sudo easy_install pip
# $ sudo pip install requests
# $ sudo pip install python-firebase



import sys, time, logging, argparse
from firebase import firebase

parser = argparse.ArgumentParser(description="communicate with the wandering-pillar restfull database.")
#parser.add_argument("mode", help="Gets the current mode from the database.")
#parser.add_Argument("--offline", help="offline mode", action="store_true") # if args.offline ....
#parser.add_argument("-b", "--battery", type=int, choices=[1, 2, 3], help="Report battery level.", default=1)
group = parser.add_mutually_exclusive_group()
group.add_argument("-g", "--get", action="store_true", help="get values from database.")
group.add_argument("-p", "--post", action="store_true", help="post values to database.")
group.add_argument("-d", "--delete", action="store_true", help="delete values from database.")

parser.add_argument("-l", "--motorLft", type=int, help="left motor values", dest="l")
parser.add_argument("-r", "--motorRgt", type=int, help="right motor values", dest="r")

args = parser.parse_args()
print args.l
