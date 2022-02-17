from minio import Minio
from urllib.parse import urlparse, urljoin
import time
import os
import sys

def get_bucketlist(url):
    """Get the listing from the object store and return a plain list of keys.
       Keys look like filenames."""

    # do some cacheing for the listing file - cache time in seconds
    cachefile = os.path.join("/tmp", os.path.basename(url) + ".txt")
    if (not os.path.exists(cachefile) or 
        (time.time() - os.path.getmtime(cachefile) > 1000)):

        # first parse the url to get the server address
        urlp = urlparse(url)
        # connect using Minio client, anonymously
        mc = Minio(urlp.netloc, secure=False)
        # get the objects in the bucket
        bl = mc.list_objects(urlp.path[1:], recursive=True)  # trim the /
        with open(cachefile, "w") as f:
            for obj in bl:
                # obj_name = (
                #     urlp.scheme + "://" + urlp.netloc + "/" + obj.object_name
                # )
                obj_name = obj.object_name
                f.write(obj_name + "\n")

    # cache file written, open and read as a list
    with open(cachefile, "r") as f:
        blist = f.read().split("\n")
    return blist
                             
if  __name__ == "__main__":
    # print a list of urls that you could grab the data from ...
    url = sys.argv[1]
    bl = get_bucketlist(url)
    for key in bl:
        print(url + "/" + key)
        
                             
                             
