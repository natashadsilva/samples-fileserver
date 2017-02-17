import os
import thread
import BaseHTTPServer
import genZips

from subprocess import call, check_output, CalledProcessError

import time
from glob import glob
from ZipServer import DownloadZipHandler
try:
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import HTTPServer as Server


def clone():
    os.chdir("static")
    print "testing git availability"
    if not (os.path.exists("samples")):
        try:
           ret = check_output(["git","clone","https://github.com/IBMStreams/samples.git"], stderr=subprocess.STDOUT)
           os.chdir("samples")
        except CalledProcessError as e:
            print "Error cloning samples: " + e.output
        return -1;

    else:
        #already exists, pull
        os.chdir("samples")
        call(["git","pull"])

    #generate zips
    #TO-DO: check for latest catalog and update
    genZips.zip_cur_directory()
    print ("Generated zips...ready to go")
    os.chdir("..")
    return 0

def start_server(root_dir):
    # Read port selected by the cloud for our application
    PORT = int(os.getenv('PORT', 8000))
    # Change current directory to avoid exposure of control files
    os.chdir(root_dir+"/static")
    httpd = Server(("", PORT), DownloadZipHandler)
    try:
      print("Start serving at port %i" % PORT)
      httpd.serve_forever()
    except KeyboardInterrupt:
      pass
    httpd.server_close()

root_dir = os.getcwd()
if clone() == 0:
    start_server(root_dir)
else:
    print "Cannot start server..Check logs."
