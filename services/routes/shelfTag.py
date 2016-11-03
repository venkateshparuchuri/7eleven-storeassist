#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request, g
from flask_restful import reqparse
from flask_restful import Resource, Api
import MySQLdb
import collections
import logging

from twisted.internet import reactor, defer, error
from twisted.internet import task
from twisted.python.failure import Failure
from twisted.web.client import getPage

import re, sys, json
import getopt

from txprinter import LPRClient # requires package python-txprinter

#UPCSERVER = 's242-srv01'
#PRINTURI = 'lpr://s242-srv02/lpz' # For testing remotely

UPCSERVER = 'store' # Store micro server
PRINTURI = 'lpr://store-ntp/lpz' # Store computer zebra print queue

exits = { 'critical' : 2,
          'warning' : 1,
          'OK' : 0,
          }
# #upc = up

def printResults(results, upc):
    print "gggggggggggg",results
    
    return "aye i am success"

def usage():
    print "Usage: zebra-print.py upc"
    sys.exit(1)

def printLabel(reactor, upc):
    #d = getPage('http://' + UPCSERVER + ':8000/product/' + upc)
    d = getPage('https://ccload.scriptbees.com/api/admin/buildto?category_name=Roller_anti&report_date=2016-10-05&store_id=36104&product_type=3&profile_id=2&profile_name=rollerGrills')

    d.addBoth(printResults, upc)
    return d

# def main():
#     # try:
#     opts, args = getopt.getopt(sys.argv[1:], "h:", ["help"])
#     task.react(printLabel, (args[0],))

# if __name__ == "__main__":
#     main()

class ShelfTag(Resource):
    # def printResults(results, upc):
    #     print "gggggggggggg",results
    #     return jsonify({"status":"success","response":results["response"]})
    #     if isinstance(results, Failure):
    #         if results.check(defer.CancelledError, error.ConnectionDone):
    #             print "Connection timeout"
    #         elif results.check(error.ConnectionRefusedError):
    #             print "Connection refused"
    #         else:
    #             print results.value
    #         raise SystemExit(exits['critical'])
    #
    #     data = json.loads(results)[0]
    #     price = float(data.get('PRICE'))
    #     if (price >= 1.0):
    #         sprice = "$%.2f" % (price,)
    #     elif (price > 0.0):
    #         sprice = "%02d_bd" % (round(price * 100),)
    #     else:
    #         sprice = 'UNKNOWN'
    #
    #     label = "^XA^FO35,25^ACN,28,14^FD%s^FS^FO70,100^ACN,28,14^FDEA^FS^FO280,90^ACN,48,24^FH^FD%s^FS^FO60,150^BEN,70^FD%s^FS^FO220,170^ACN,28,14^XZ" % (data.get('NAME'), sprice, upc)
    #
    #     try:
    #         if PRINTURI and PRINTURI[:6] == 'lpr://':
    #             hostname, queue = PRINTURI[6:].split('/')
    #             if hostname and queue:
    #                 lpc = LPRClient(hostname)
    #                 return lpc.printJob(queue, str(label))
    #
    #     except Exception as e:
    #         print 'Failed to create LPRClient'
    #         raise SystemExit(exits['critical'])
    #
    #     return None
    #
    # def usage():
    #     print "Usage: zebra-print.py upc"
    #     sys.exit(1)

    # def printLabel(reactor, upc):
    #     #d = getPage('http://' + UPCSERVER + ':8000/product/' + upc)
    #     d = getPage('https://ccload.scriptbees.com/api/admin/buildto?category_name=Roller_anti&report_date=2016-10-05&store_id=36104&product_type=3&profile_id=2&profile_name=rollerGrills')
    #
    #     d.addBoth(printResults, upc)
    #     return d

    def get(self):
        upc = request.args.get("upc")

        sys.argv = upc
        opts, args = getopt.getopt(sys.argv[1:], "h:", ["help"])
        task.react(printLabel, (args[0],))
        # print request.args.get("upc")
        # task.react(printLabel,(''))
