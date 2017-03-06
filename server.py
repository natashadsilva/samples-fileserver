import os
import thread
import BaseHTTPServer
import genZips

from subprocess import call, check_output, CalledProcessError
import subprocess

import time
from glob import glob
from ZipServer import DownloadZipHandler
try:
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import HTTPServer as Server

#Clone the samples repository
#This way, we can generate the latest zips on demand.
#ideally, we would run this script every time the samples repoitory was changed.



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
start_server(root_dir)
