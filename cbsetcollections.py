#!/usr/bin/env python

import os
import sys
import argparse
import pprint
from lib.mc_bin_client import *
from lib.couchbaseConstants import *

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-u", "--user", help="User", required=True)
    parser.add_argument("-p", "--password", help="Password", required=True)
    parser.add_argument("-n", "--node", help="Node host:port", required=True)
    parser.add_argument("-b", "--bucket", help="Bucket name", required=True)
    parser.add_argument("-m", "--manifest", help="Manifest file", required=True)

    args = parser.parse_args()

    host, port = args.node.split(":")

    conn = MemcachedClient(host, int(port))

    conn.sasl_auth_plain(args.user, args.password)

    conn.hello([HELLO_COLLECTIONS])

    conn.bucket_select(args.bucket);

    jsonManifestFile = open(args.manifest, "r")
    json = jsonManifestFile.read()
    print "Setting collections - {}".format(json)
    conn.set_collections(json)
    jsonManifestFile.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
