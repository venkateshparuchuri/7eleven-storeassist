#! /usr/bin/python
from flask_restful import reqparse
from flask_restful import Resource
from flask import  jsonify, abort, make_response, request, g
import MySQLdb
import collections
import logging
import sys
import os
import datetime as DT
import time
from sets import Set
from sqlobject import *

from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from jsonschema import validate

prodstores = Set(xrange(1,140)) - Set([13,])


class MoneyOrders (SQLObject):
    SerialNo = StringCol (length = 20, notNone = True, alternateID = True)
    DocValue = DecimalCol (size = 6, precision = 2, notNone = True)
    PurchTS = DateTimeCol (notNone = True)
    Store = IntCol (notNone = True)
    TransNo = IntCol (notNone = True)
    Voided = BoolCol (notNone = True, default = False)
    VoidTS = DateTimeCol ()
    VoidStore = IntCol ()
    Cleared = BoolCol (notNone = True, default = False)
    Cashed = BoolCol (default = False)

    serialkey = DatabaseIndex('SerialNo', unique = True)
    class sqlmeta:
        cacheValues = False

class MoForms(SQLObject):
    Timestamp = DateTimeCol(notNone = True, default = sqlbuilder.func.NOW())
    TimestampMs = DecimalCol(size=3, precision=0, notNone = True)
    RangeBegin = DecimalCol(size=10, precision=0, notNone = True)
    RangeEnd   = DecimalCol(size=10, precision=0, notNone = True)
    LocationType = EnumCol(enumValues = ['office','supervisor','store','printer','shredder','sold'], notNone = True)
    Location = StringCol(length=80, varchar=True, notNone = True)
    ActionedBy = StringCol(length=40, varchar=True)
    Active = BoolCol (notNone = True)
    rangeIndex = DatabaseIndex('RangeBegin','RangeEnd')
    class sqlmeta:
        cacheValues = False

class MoneyOrderAuditLog (SQLObject):
    SerialNo = StringCol (length = 20, notNone = True)
    Method = StringCol (length = 10, notNone = True)
    Store = IntCol (notNone = True)
    TS = DateTimeCol ()
    Success = BoolCol (notNone = True, default = False)

    moalserialkey = DatabaseIndex('SerialNo', 'TS', unique = True)
    class sqlmeta:
        cacheValues = False

## inquire

MoneyOrderInquireSchema = {
    'type': 'object',
    'properties': {
        'SerialNo': {'type': 'string'},
		'Store': {'type': 'integer'}
    },
	"required": ["SerialNo","Store"]
}


class MoneyOrderInquireSchemaApiInputs(Inputs):
    json = [JsonSchema(schema=MoneyOrderInquireSchema)]

class MoneyOrderInquire(Resource):

    def post(self):

        logger = logging.getLogger("MoneyOrderInquire post")
        logger.info('Entered into MoneyOrderInquire post  method')

        inputs = MoneyOrderInquireSchemaApiInputs(request)
        if not inputs.validate():
            return jsonify(success=False, errors=inputs.errors)

        try:
            mysql_url = "mysql://" + g.moneyorder_user + ":" + g.moneyorder_password + "@" + g.moneyorder_server + "/" + g.moneyorder_db
            sqlhub.processConnection = connectionForURI (mysql_url)

            MoneyOrders.createTable (ifNotExists = True)
            MoForms.createTable (ifNotExists = True)
            MoneyOrderAuditLog.createTable (ifNotExists = True)

            inquire = request.json
            document = MoneyOrders.bySerialNo (inquire[ 'SerialNo' ])

        except:
            return jsonify({"status":"failure","response": "Invalid document"})

        if document and ((document.Store in prodstores) == (inquire [ 'Store' ] in prodstores)):
            MoneyOrderAuditLog(SerialNo = inquire [ 'SerialNo' ], Method = 'inquiry', Store = inquire [ 'Store' ], TS = DT.datetime.now(), Success = True)
            return jsonify({"status":"success","response":str(document.DocValue),"Cashed":document.Cashed})

        else:
            MoneyOrderAuditLog(SerialNo = inquire [ 'SerialNo' ], Method = 'inquiry', Store = inquire [ 'Store' ], TS = DT.datetime.now(), Success = False)
            return jsonify({"status":"failure","response": "HTTP_NOT_FOUND"})

        logger.info('Exited from the MoneyOrderInquire Method')

## cash

MoneyOrderCashSchema = {
    'type': 'object',
    'properties': {
        'SerialNo': {'type': 'string'},
		'Store': {'type': 'integer'}
    },
	"required": ["SerialNo","Store"]
}


class MoneyOrderCashSchemaApiInputs(Inputs):
    json = [JsonSchema(schema=MoneyOrderCashSchema)]

class MoneyOrderCash(Resource):

    def post(self):

        logger = logging.getLogger("MoneyOrderCash post")
        logger.info('Entered into MoneyOrderCash post  method')

        inputs = MoneyOrderCashSchemaApiInputs(request)
        if not inputs.validate():
            return jsonify(success=False, errors=inputs.errors)

        try:
            mysql_url = "mysql://" + g.moneyorder_user + ":" + g.moneyorder_password + "@" + g.moneyorder_server + "/" + g.moneyorder_db
            sqlhub.processConnection = connectionForURI (mysql_url)

            MoneyOrders.createTable (ifNotExists = True)
            MoForms.createTable (ifNotExists = True)
            MoneyOrderAuditLog.createTable (ifNotExists = True)

            cash = request.json
            document = MoneyOrders.bySerialNo (cash[ 'SerialNo' ])

        except:
            return jsonify({"status":"failure","response": "Invalid document"})

        found = (document and ((document.Store in prodstores) == (cash [ 'Store' ] in prodstores)))

        if found and (document.Cashed == True):
            MoneyOrderAuditLog(SerialNo = cash [ 'SerialNo' ], Method = 'cash', Store = cash [ 'Store' ], TS = DT.datetime.now(), Success = False)
            return jsonify({"status":"failure","response": "HTTP_NOT_FOUND"})

        elif found:
            document.Cashed = True
            MoneyOrderAuditLog(SerialNo = cash [ 'SerialNo' ], Method = 'cash', Store = cash [ 'Store' ], TS = DT.datetime.now(), Success = True)
            return jsonify({"status":"success"})

        else:
            MoneyOrderAuditLog(SerialNo = cash [ 'SerialNo' ], Method = 'cash', Store = cash [ 'Store' ], TS = DT.datetime.now(), Success = False)
            return jsonify({"status":"failure","response": "HTTP_NOT_FOUND"})

        logger.info('Exited from the MoneyOrderCash Method')
