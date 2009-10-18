import sys,os
sys.path.append(os.path.dirname(__file__))
import common
import modules
import utils
from silpa import Silpa
if __name__ == '__main__':
    print("Silpa server loading ....")
    try:
        from wsgiref import simple_server
        silpa = Silpa()
        simple_server.make_server('', 8080, silpa.serve).serve_forever()
    except KeyboardInterrupt:
        print("Ctrl-C caught, Silpa server exiting...")



