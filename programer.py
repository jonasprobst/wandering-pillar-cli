import argparse, json, requests, logging, sys, datetime

def main(argv):
    #wandering pillar protocoll
    CONST_CMD_STOP = 0
    CONST_CMD_FORWARD = 1
    CONST_CMD_BACKWARD = 2
    CONST_CMD_RIGHT = 3
    CONST_CMD_LEFT = 4

    #setup logging
    logging.basicConfig(filename="wapi.log", level=logging.DEBUG)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info("\n\n>> PROGRAMMER.PY - {0}".format(now))

    #hack to disable security warning. CHeck the follwoing docs. i know it's not pretty...
    #https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
    logging.captureWarnings(True)

    #TODO: make commands exculsive!
    parser = argparse.ArgumentParser(description="programm the wandering pillar.", version="0.1")
    parser.add_argument("id", type=int, help="device id")
    parser.add_argument("-u", "--baseurl", default="https://wapi.firebaseio.com", dest="baseurl", help="firebase baseurl.")
    parser.add_argument("-s", "--step", type=int, default=-1, help="step number")
    parser.add_argument("-c", "--command", choices=["stop", "forward", "backward", "left", "right"], dest="command", help="command")
    parser.add_argument("-d", "--duration", type=int, default=60, help="duration in secs")
    parser.add_argument("-g", "--gear", type=int, choices=[1, 2], default=1, help="gear")
    parser.add_argument("--clear", dest="clear", action='store_true', help="clear current program (executes first)")
    parser.add_argument("--display", dest="display", action='store_true', help="display current program (executes last)")
    args = parser.parse_args()

    if args.clear:
        #clear current program
        url = args.baseurl + "/devices/{0}/program.json".format(args.id)
        try:
            r = requests.delete(url)
        except Exception as e:
            logging.debug("Error - failed to delete program: {0}".format(e))
            sys.exit(2)


    if args.command:
        #add step
        if args.step < 0:
            #add step to the end -> last step number +1
            url = args.baseurl + "/devices/{0}/program.json".format(args.id)
            try:
                r = requests.get(url)
            except Exception as e:
                logging.debug("Error - failed to load program: {0}".format(e))
                sys.exit(2)
            program = r.json()

            if(program):
                step = len(program)
            else:
                step = 0
        else:
            step = args.step

        program = {}
        program['command'] = args.command
        program['duration'] = args.duration
        program['gear'] = args.gear

        url = args.baseurl + "/devices/{0}/program/{1}.json".format(args.id, step)
        try:
            r = requests.put(url, json=program)
        except Exception as e:
            logging.debug("Error - failed to put program: {0}".format(e))
            sys.exit(2)

    if args.display:
        #display current program
        url = args.baseurl + "/devices/{0}/program.json".format(args.id)
        try:
            r = requests.get(url)
            print json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            logging.debug("Error - failed to display program: {0}".format(e))
            sys.exit(2)

    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
