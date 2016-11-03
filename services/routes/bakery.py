from flask_restful import reqparse
from flask_restful import Resource
from flask import  jsonify, abort, make_response, request, g
import MySQLdb
import collections
import logging

from flask_inputs import Inputs
from wtforms.validators import DataRequired

from flask_inputs.validators import JsonSchema
from jsonschema import validate


# BakeryOrdersSchema = {
#     'type': 'object',
#     'properties': {
#         'store_id' : {'type': 'integer'},
#         'date' : {'type': 'string'}
#     },
#     "required": ["store_id","date"]
# }
#
# class BakeryOrders(Inputs):
#     args = {
#         'store_id': [DataRequired(message='Store ID Required')],
#         'date': [DataRequired(message='Date Required')]
#     }
#
# class BakeryOrdersApiInputs(Inputs):
#     json = [JsonSchema(schema=BakeryOrdersSchema)]

class BakeryOrders(Resource):
    def get(self):
        logger = logging.getLogger("BakeryOrders")
        logger.info('Entered into BakeryOrders get  method')

        try:
            # inputs = BakeryOrders(request)
            # if not inputs.validate():
            #     return jsonify(success=False, errors=inputs.errors)

            store_id = int(request.args.get("store_id"))
            date = str(request.args.get("date"))
            cursor = g.appdbNew.cursor()
        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """  SELECT ts.id, tr.id AS requests_id, cast(tc.sku as char) as sku, cast(ts.nbr as char) as nbr, cast(ts.descr as char) as descr,
              cast(ts.pick_nbr as char) as pick_nbr, cast(tr.on_hand_qty as char) as on_hand_qty, cast(tr.return_qty as char) as return_qty, tr.active
              from tr_skus ts
              inner join tr_sku_custs tc on tc.sku = ts.nbr
              left outer join tr_requests tr on ts.nbr = tr.nbr and tr.store = %s and tr.date = %s
              where tc.cust = 1 and ts.active = 1 and tc.display = 1
              order by pick_nbr """
        cursor.execute(query,(store_id, date))
        rv = cursor.fetchall()

        logger.info('Exited from the BakeryOrders Method')
        return jsonify({"status":"success","response":rv})

    def post(self):
        logger = logging.getLogger("BakeryOrders post")
        logger.info('Entered into BakeryOrders method')

        try:
            BakeryOrders = request.json
            cursor = g.appdbNew.cursor()
        except:
            logger.error('Either db connection or date calculation error', exc_info=True)

        for value in BakeryOrders:
            if int(value['order_id']) > 0:
                if value['on_hand_qty'] == 'null' and value['return_qty'] == 'null':
                    query = """ DELETE from tr_requests where id = %s """
                    cursor.execute(query, (value['order_id'], ))
                    g.appdbNew.commit()

                else:
                    updatequery = """ UPDATE tr_requests SET on_hand_qty = %s, return_qty = %s, last_modified = %s, active = %s WHERE id = %s """
                    cursor.execute(updatequery, (value["on_hand_qty"], value["return_qty"], value["last_modified"], value["active"], value["order_id"]))
                    g.appdbNew.commit()
            else:
                query = """ INSERT INTO tr_requests (store, nbr, descr, on_hand_qty, return_qty, date, active) VALUES (%s, %s, %s, %s, %s, %s, %s) """
                cursor.execute(query, (value["store_id"], value["nbr"], value["descr"], value["on_hand_qty"], value["return_qty"], value["date"], value["active"]))
                g.appdbNew.commit()

        logger.info('Exited from BakeryOrders post method')
        return jsonify({"status":"success"})

class Message(Resource):
    def get(self):
        logger = logging.getLogger("Message get")
        logger.info('Entered into Message get  method')

        try:
            store_id = int(request.args.get("store_id"))
            cursor = g.messagedb.cursor()
        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """  SELECT m.message_id, m.subject, m.body, ms.read, cast(m.date_sent as char) AS date_sent, cast(time_sent as char) time_sent
              FROM message m
              inner join message_store ms on m.message_id = ms.message_id
              where ms.Store = %s order by ms.read = 0 """
        cursor.execute(query,(store_id, ))
        rv = cursor.fetchall()

        logger.info('Exited from the Message Method')
        return jsonify({"status":"success","response":rv})

    def put(self):
        logger = logging.getLogger("Message PUT")
        logger.info('Entered into Message Update method')

        try:
            message_id = int(request.json["message_id"])
            read = int(request.json["read"])
            store_id = int(request.json["store_id"])
            cursor = g.messagedb.cursor()
        except:
            logger.error('Either connection problem or unable to get url parameters', exc_info=True)

        completeQuery = """ UPDATE message_store ms SET ms.read = %s WHERE ms.message_id = %s and ms.store = %s """
        cursor.execute(completeQuery, (read, message_id, store_id))
        g.messagedb.commit()

        logger.info('Exited from Message PUT Method')
        return jsonify({"status":"success"})

class ManualGasDipReport(Resource):
    def get(self):
        logger = logging.getLogger("ManualGasDipReport get")
        logger.info('Entered into ManualGasDipReport get  method')

        try:
            cursor = g.appdb.cursor()
            store_id = int(request.args.get("store_id"))
            reported_date = str(request.args.get("date"))

        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """ SELECT dp.tankno AS tank, dp.grade, dp.descr AS description, CAST(dp.water_inches as char) AS water,
              dk.init, dk.dipped_yn, CAST(dp.bdate as char) AS Date
              FROM drpmpdip dp
              inner join drpmpchk dk on dp.store = dk.store
              where dp.store = %s and dp.bdate = %s """
        cursor.execute(query,(store_id, reported_date))
        rv = cursor.fetchall()

        if len(rv) > 0:
            return jsonify({"status":"success","response":rv})

        else:
            query = """ SELECT dp.tankno AS tank, dp.grade, dp.descr AS description, CAST(dp.water_inches as char) AS water,
                  dk.init, dk.dipped_yn, CAST(dp.bdate as char) AS Date
                  FROM drpmpdip dp
                  inner join drpmpchk dk on dp.store = dk.store
                  where dp.store = %s and dp.bdate = (SELECT max(bdate) FROM drpmpdip where store = %s) """
            cursor.execute(query,(store_id, reported_date))
            rv = cursor.fetchall()
            return jsonify({"status":"success","response":rv})

        logger.info('Exited from the ManualGasDipReport get Method')


    def post(self):
        logger = logging.getLogger("ManualGasDipReport post")
        logger.info('Entered into ManualGasDipReport method')

        try:
            GasDipReport = request.json
            cursor = g.appdb.cursor()
        except:
            logger.error('Either db connection or date calculation error', exc_info=True)

        query = """ UPDATE drpmpchk SET init = %s, dipped_yn = %s WHERE store = %s AND bdate = %s """
        cursor.execute(query, (GasDipReport["init"], GasDipReport["dipped_yn"], GasDipReport["store_id"], GasDipReport["reported_date"]))
        g.appdb.commit()

        for value in GasDipReport["DipReport"]:
            updatequery = """ UPDATE drpmpdip SET water_inches = %s WHERE store = %s AND bdate = %s AND tankno = %s """
            cursor.execute(updatequery, (value["water"], GasDipReport["store_id"], GasDipReport["reported_date"], value["tank"]))
            g.appdb.commit()

        return jsonify({"status":"success"})
        logger.info('Exited from the ManualGasDipReport Method')

class DipReportByDate(Resource):
    def get(self):
        logger = logging.getLogger("DipReportByDate get")
        logger.info('Entered into DipReportByDate get  method')

        try:
            cursor = g.appdb.cursor()
            store_id = int(request.args.get("store_id"))
            reported_date = str(request.args.get("date"))

        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """ SELECT dp.tankno AS tank, dp.grade, dp.descr AS description, dk.init, dk.dipped_yn, CAST(dp.bdate as char) AS Date
              FROM drpmpdip dp
              inner join drpmpchk dk on dp.store = dk.store
              where dp.store = %s and dp.bdate = %s """
        cursor.execute(query,(store_id, reported_date))
        rv = cursor.fetchall()

        return jsonify({"status":"success","response":rv})
        logger.info('Exited from the DipReportByDate Method')
