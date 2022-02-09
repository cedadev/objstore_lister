
import xml.etree.ElementTree as ET
import urllib.request
import time
import os
import sys

def get_bucketlist(url):
    """Get the listing from the object store and return a plain list of keys.
       Keys look like filenames."""

    # do some cacheing for the listing file
    cachefile = os.path.join("/tmp", os.path.basename(url) + ".xml")
    if not os.path.exists(cachefile) or os.path.getmtime(cachefile) - time.time() > 1000:
        with urllib.request.urlopen(url) as f:
            content = f.read()
        with open(cachefile, "wb") as f:
            f.write(content)

    # extract the keys into a plain list
    tree = ET.parse(cachefile)
    root = tree.getroot()
    blist = []
    for key in root.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents/{http://s3.amazonaws.com/doc/2006-03-01/}Key'):
        blist.append(key.text)
    return blist

                             
if  __name__ == "__main__":
    # print a list of urls that you could grab the data from ...
    url = sys.argv[1]
    bl = get_bucketlist(url)
    for key in bl:
        print(url + "/" + key)
        
                             
                             
