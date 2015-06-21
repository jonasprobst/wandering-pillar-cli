import argparse, json, requests, logging, sys, datetime

#wandering pillar protocoll
CONST_CMD_STOP = 0
CONST_CMD_FORWARD = 1
CONST_CMD_BACKWARD = 2
CONST_CMD_RIGHT = 3
CONST_CMD_LEFT = 4
CONST_CMD_RESTART = 5

def getStep(url):
    try:
        r = requests.get(url)
        print r.status_code
        print r.text
        if r.status_code == 200:
            program = r.json()
            cmd = ""
            if program['command'] == "stop":
                cmd = CONST_CMD_STOP
            elif program['command'] == "forward":
                cmd = CONST_CMD_FORWARD
            elif program['command'] == "backward":
                cmd = CONST_CMD_BACKWARD
            elif program['command'] == "right":
                cmd = CONST_CMD_RIGHT
            elif program['command'] == "left":
                cmd = CONST_CMD_LEFT
            else:
                cmd = CONST_CMD_STOP


            print str(cmd) + "," + str(program['duration']) + "," + str(program['gear'])


        else:
            #set to manual mode
            print CONST_CMD_STOP

    except Exception as e:
        print CONST_CMD_STOP
        logging.debug("GET-Error: {0}".format(e))
        sys.exit(1)


def main(argv):


    #setup logging
    logging.basicConfig(filename="wapi.log", level=logging.DEBUG)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info("\n\n>> NEXTSTEP.PY - {0}".format(now))

    #hack to disable security warning. CHeck the follwoing docs. i know it's not pretty...
    #https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
    logging.captureWarnings(True)

    parser = argparse.ArgumentParser(description="check the current mode (auto or manual) of a wandering pillar.", version="0.1")
    parser.add_argument("id", type=int, help="device id")
    parser.add_argument("mode", choices=["a", "auto", "m", "manual"], help="current mode")
    parser.add_argument("-u", "--baseurl", default="https://wapi.firebaseio.com", dest="baseurl", help="firebase baseurl.")
    parser.add_argument("-s", "--step", type=int, help="step number")

    args = parser.parse_args()

    if args.mode == "auto" or args.mode == "a":
        #get programm
        url = args.baseurl + "/devices/{0}/program.json".format(args.id)
        try:
            r = requests.get(url)
        except Exception as e:
            #stop if anything is fishy
            print CONST_CMD_STOP
            logging.debug("POST-Error: {0}".format(e))

        program = r.json()
        if program:
            #what's the next step??
            if args.step:
                #resuming
                if args.step >= len(program):
                    #we've reached the end of the program
                    #loop back
                    print CONST_CMD_RESTART
                else:
                    #get
                    url = args.baseurl + "/devices/{0}/program/{1}.json".format(args.id, args.step)
                    getStep(url)
            else:
                #starting
                #get step 0
                url = args.baseurl + "/devices/{0}/program/{1}.json".format(args.id, 0)
                getStep(url)
        else:
            #there is no program
            print CONST_CMD_STOP

    else:
        #manual mode
        url = args.baseurl + "/devices/{0}/cmd.json".format(args.id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                cmd = r.json()
                if cmd == "stop":
                    print CONST_CMD_STOP
                elif cmd == "forward":
                    print CONST_CMD_FORWARD
                elif cmd == "backward":
                    print CONST_CMD_BACKWARD
                elif cmd == "right":
                    print CONST_CMD_RIGHT
                elif cmd == "left":
                    print CONST_CMD_LEFT
            else:
                #set to manual mode
                print CONST_CMD_STOP

        except Exception as e:
            print CONST_CMD_STOP
            logging.debug("GET-Error: {0}".format(e))

    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
