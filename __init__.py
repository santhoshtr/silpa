import sys,os
sys.path.append(os.path.dirname(__file__))
import common
import modules
import utils
from silpa import Silpa
if __name__ == '__main__':
    print("Silpa server loading ...")
    port = 8080
    if len(sys.argv)> 1:
        port = int(sys.argv[1])
    try:
        from wsgiref import simple_server
        silpa = Silpa()
        print("Listening on port : " + str(port))
        print("Silpa is ready!!!")
        simple_server.make_server('', port, silpa.serve).serve_forever()
    except KeyboardInterrupt:
        print("Ctrl-C caught, Silpa server exiting...")



