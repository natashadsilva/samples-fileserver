import os
import json
import sys
import urllib

#tests that the links used to download zips from the server work.
#failed samples are written to a file called failed.txt
from subprocess import call, check_output


server = "https://streams-github-samples.mybluemix.net/?get="
if len(sys.argv) > 1 and sys.argv[1] == "local":
    print "Testing local server"
    server = "http://127.0.0.1:8000/?get="

#change the server url to test localhost if needed.
#1. Read the JSON file that holds all the catalog entries
samples_dir =os.getcwd()+ "/../static/samples/"
current_dir = os.getcwd()
os.chdir(samples_dir)
ret = call(["python","generate-full-catalog-json.py"])
if ret !=0 :
    print "Failed to generate catalog"

file = open("full-catalog.json", "r")
os.chdir(current_dir)
errors =open("failed.txt","w")
jay = json.load(file)
existing_zip_dir= samples_dir
base ="https://github.com/IBMStreams/samples/tree/master/"
os.chdir("results")
#for each element in the json file, get the url
for elem in jay:
   url = elem["url"]
   print url

   idx = url.index(base) + len(base)
   url = url[idx:]
   #escape special characters
   escaped_url= urllib.quote(url)
   print "new url =" + url
   zipfile = url.split("/")[1]

   if (os.path.exists(zipfile)):
        print "Error " + zipfile + " already exists"
   else:
       #download the zip from the server using curl
        call(["curl","-O", server + escaped_url])
        print os.getcwd()
        escaped_zip_name = urllib.quote(zipfile)
        #if the file was downloaded
        if os.path.exists(escaped_zip_name):
            #compare it with what we have locally
            ret = call(["diff", escaped_zip_name, existing_zip_dir + url + "/" + zipfile+".zip"])
            if (ret != 0):
                errors.write("downloaded zip mismatch " +escaped_zip_name + "\n")
                errors.write("\turl = " +url + "  zipfile = " + escaped_zip_name + "requested " + server+escaped_url+"\n")
        else:
            #if an error occured downloading, print it
            print "error, downloading " + escaped_zip_name + "failed"
            errors.write("download error " + escaped_zip_name + "\n")
            errors.write("\turl = " +url + "  zipfile = " + zipfile + "requested " + server+escaped_url+"\n")

os.chdir("..")

file.close()
errors.close()
