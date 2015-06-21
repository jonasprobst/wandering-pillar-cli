import argparse, json, requests, logging, sys, datetime

def setMode(url, mode):
    try:
        r = requests.put(url, json=mode)
    except Exception as e:
        logging.debug("POST-Error: {0}".format(e))
        return False
    return True

def main(argv):
    #wandering pillar protocoll
    CONST_MODE_MAN = 0
    CONST_MODE_AUTO = 1

    #setup logging
    logging.basicConfig(filename="wapi.log", level=logging.DEBUG)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info("\n\n>> MODE.PY - {0}".format(now))

    #hack to disable security warning. CHeck the follwoing docs. i know it's not pretty...
    #https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
    logging.captureWarnings(True)

    parser = argparse.ArgumentParser(description="check the current mode (auto or manual) of a wandering pillar.", version="0.1")
    parser.add_argument("id", type=int, help="device id")
    parser.add_argument("-u", "--baseurl", default="https://wapi.firebaseio.com", dest="baseurl", help="firebase baseurl.")
    parser.add_argument("-m", "--mode", dest="mode", choices=["auto", "manual"], help="set mode (post)" )
    args = parser.parse_args()

    url = args.baseurl + "/devices/{0}/mode.json".format(args.id)

    if args.mode:
        mode = str(args.mode)
        setMode(url, mode)

    else:
        #send get requests
        try:
            r = requests.get(url)
            if r.status_code == 200 and r.json() == "auto":
                #set to auto mode
                print CONST_MODE_AUTO
            else:
                #set to manual mode
                print CONST_MODE_MAN

        except Exception as e:
            print CONST_MODE_MAN
            logging.debug("GET-Error: {0}".format(e))

    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
