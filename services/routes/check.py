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


class CardCheckReport(Resource):
    def get(self):
        logger = logging.getLogger("CardCheckReport")
        logger.info('Entered into CardCheckReport get  method')

        try:
            cursor = g.appdb.cursor()
            store_id = request.args.get("store_id")
            reported_date = str(request.args.get("reported_date"))
        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """ SELECT CAST(reported_time as char) AS time FROM card_reader_report where store_id = %s and reported_date = %s """
        cursor.execute(query, (store_id, reported_date ))
        rv = cursor.fetchall()

        logger.info('Exited from the CardCheckReport get Method')
        return jsonify({"status":"success","response":rv})

    def post(self):
        logger = logging.getLogger("CardCheckReport post")
        logger.info('Entered into CardCheckReport method')

        try:
            CardCheckReport = request.json
            cursor = g.appdb.cursor()
        except:
            logger.error('Either db connection or date calculation error', exc_info=True)

        query = """ INSERT INTO card_reader_report (store_id, employee_initials, reported_date, reported_time) VALUE (%s, %s, %s, %s) """
        cursor.execute(query, (CardCheckReport['store_id'], CardCheckReport['employee_initials'], CardCheckReport['reported_date'], CardCheckReport['reported_time']))
        g.appdb.commit()
        newID = cursor.lastrowid

        logger.info('Exited from the CardCheckReport Method')
        return jsonify({"status":"success","response":newID})

class ItEquipmentReport(Resource):
    def get(self):
        logger = logging.getLogger("ItEquipmentReport")
        logger.info('Entered into ItEquipmentReport get  method')

        try:
            cursor = g.appdb.cursor()
            store_id = request.args.get("store_id")
            reported_date = str(request.args.get("reported_date"))
        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """ SELECT CAST(reported_time as char) AS time FROM it_payment_report where store_id = %s and reported_date = %s """
        cursor.execute(query, (store_id, reported_date ))
        rv = cursor.fetchall()

        logger.info('Exited from the ItEquipmentReport get Method')
        return jsonify({"status":"success","response":rv})

    def post(self):
        logger = logging.getLogger("ItEquipmentReport post")
        logger.info('Entered into ItEquipmentReport method')

        try:
            ItEquipmentReport = request.json
            cursor = g.appdb.cursor()
        except:
            logger.error('Either db connection or date calculation error', exc_info=True)

        query = """ INSERT INTO it_payment_report (store_id, employee_initials, reported_date, reported_time) VALUE (%s, %s, %s, %s) """
        cursor.execute(query, (ItEquipmentReport['store_id'], ItEquipmentReport['employee_initials'], ItEquipmentReport['reported_date'], ItEquipmentReport['reported_time']))
        g.appdb.commit()
        newID = cursor.lastrowid

        logger.info('Exited from the ItEquipmentReport Method')
        return jsonify({"status":"success","response":newID})

class ChangeOrder(Resource):
    def get(self):
        logger = logging.getLogger("ChangeOrder")
        logger.info('Entered into ChangeOrder get  method')

        try:
            cursor = g.appdb.cursor()
            store_id = str(request.args.get("store_id"))
            date = str(request.args.get("date"))
            changeorderId = int(request.args.get("changeorderId"))
        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        if changeorderId == 0:
            query = """ SELECT  cod.id, co.id AS changeOrderId, c.id AS currencyId, c.name, cast(c.value as char) as Amount, CAST(cod.order_amount as char) as order_amount ,
                  co.order_status FROM change_order_details cod
                  inner join change_order co on co.id = cod.change_order_id and co.store_id = %s and co.ordered_time = %s
                  right outer join currency c on cod.currency_id = c.id """
            cursor.execute(query, (store_id, date))
            rv = cursor.fetchall()
        elif changeorderId > 0:
            query = """ SELECT cod.id, c.id AS currencyId, co.ordered_by, c.name, cast(c.value as char) as Amount, CAST(cod.order_amount as char) as order_amount,
                  co.order_status AS Status FROM currency c
                  left outer join change_order_details cod on cod.change_order_id = %s and c.id = cod.currency_id
                  left outer  join change_order co on co.id = cod.change_order_id """
            cursor.execute(query, (changeorderId, ))
            rv = cursor.fetchall()

        logger.info('Exited from the ChangeOrder Method')
        return jsonify({"status":"success","response":rv})

    def post(self):
        logger = logging.getLogger("ChangeOrder post")
        logger.info('Entered into ChangeOrder method')

        try:
            changeOrder = request.json
            cursor = g.appdb.cursor()
        except:
            logger.error('Either db connection or date calculation error', exc_info=True)

        if int(changeOrder["orderID"]) == 0:
            storeId = changeOrder['store_id']
            orderBy = changeOrder['orderBy']
            orderTime = changeOrder['orderTime']
            orderStatus = changeOrder['orderStatus']
            receivedStatus = changeOrder['receivedStatus']
            query = """ INSERT INTO change_order (store_id, ordered_by, ordered_time, order_status, received_status) VALUES (%s, %s, %s, %s, %s) """
            cursor.execute(query, (storeId, orderBy, orderTime, orderStatus, receivedStatus))
            g.appdb.commit()
            newID = cursor.lastrowid
        else:
            query = """ UPDATE change_order SET order_status = %s WHERE id = %s """
            cursor.execute(query, (changeOrder['orderStatus'], changeOrder["orderID"]))
            g.appdb.commit()
            newID = changeOrder["orderID"]

        for i in changeOrder["changeOrderDetails"]:
            if i["changeorderId"] == 0:
                sub_query = """  INSERT INTO change_order_details (change_order_id, currency_id, order_amount) VALUES (%s, %s, %s) """
                cursor.execute(sub_query, (newID, i["currencyId"], i['orderQuantity']))

            elif i["orderQuantity"] == 0 and i["changeorderId"] > 0:
                delete = """ DELETE from change_order_details where id = %s """
                cursor.execute(delete, (i["changeorderId"], ))

            elif i["changeorderId"] > 0:
                update = """ UPDATE change_order_details set order_amount = %s where id = %s """
                cursor.execute(update, (i["orderQuantity"], i["changeorderId"]))
            g.appdb.commit()

        logger.info('Exited from ChangeOrder post method')
        return jsonify({"status":"success", "response":newID})

class ChangeOrderHistory(Resource):
    def get(self):
        logger = logging.getLogger("ChangeOrderHistory")
        logger.info('Entered into ChangeOrderHistory get  method')

        try:
            store_id = int(request.args.get("store_id"))
            cursor = g.appdb.cursor()
        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """ SELECT co.id AS changeOrderID, co.ordered_by, cast(Date_Format(co.ordered_time,'%%Y-%%m-%%d') as char) As Date,
              cast(sum(cod.order_amount) as char) AS Total, co.order_status, co.received_status FROM change_order co
              inner join change_order_details cod on cod.change_order_id = co.id
              where co.store_id = %s group by co.id order by changeOrderID desc """
        cursor.execute(query,(store_id, ))
        rv = cursor.fetchall()

        logger.info('Exited from the ChangeOrderHistory Method')
        return jsonify({"status":"success","response":rv})

    def post(self):
        logger = logging.getLogger("ChangeOrderHistory post")
        logger.info('Entered into ChangeOrderHistory method')

        try:
            orderHistory = request.json
            cursor = g.appdb.cursor()
        except:
            logger.error('Either db connection or date calculation error', exc_info=True)

        query = """ SELECT co.id AS changeOrderID, co.ordered_by, cast(Date_Format(co.ordered_time,'%%Y-%%m-%%d') as char) As Date,
              cast(sum(cod.order_amount) as char) AS Total, co.order_status, co.received_status FROM change_order co
              inner join change_order_details cod on cod.change_order_id = co.id
              where co.store_id = %s and Date_Format(co.ordered_time,'%%Y-%%m-%%d') = %s
              group by co.id order by changeOrderID desc """
        cursor.execute(query, (orderHistory['store_id'], orderHistory['date']))
        rv = cursor.fetchall()

        logger.info('Exited from the ChangeOrderHistory Method')
        return jsonify({"status":"success","response":rv})

class ChangeOrderReceived(Resource):
    def get(self):
        logger = logging.getLogger("ChangeOrderReceived")
        logger.info('Entered into ChangeOrderReceived get  method')

        try:
            cursor = g.appdb.cursor()
            changeorderId = int(request.args.get("changeorderId"))
        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """ SELECT cod.id, co.id AS changeOrderID, co.ordered_by, c.id as currency, c.name, cast(c.value as char) as Amount,
              cast(Date_Format(co.ordered_time,'%%Y-%%m-%%d') as char) As orderedDate,  co.received_by,  co.received_status,
              CAST(cod.order_amount as char) AS order_amount , CAST(cod.received_amount as char) AS received_amount
              FROM change_order_details cod
              inner join change_order co on co.id = cod.change_order_id and cod.change_order_id = %s
              right outer join currency c on cod.currency_id = c.id """
        cursor.execute(query, (changeorderId, ))
        rv = cursor.fetchall()

        logger.info('Exited from the ChangeOrderReceived Method')
        return jsonify({"status":"success","response":rv})

    def post(self):
        logger = logging.getLogger("ChangeOrderReceived post")
        logger.info('Entered into ChangeOrderReceived method')

        try:
            ChangeOrderReceived = request.json
            cursor = g.appdb.cursor()
        except:
            logger.error('Either db connection or date calculation error', exc_info=True)

        query = """ UPDATE change_order SET received_by = %s, received_time = %s, received_status = %s WHERE id = %s """
        cursor.execute(query, (ChangeOrderReceived["receivedBy"], ChangeOrderReceived["receivedDate"], ChangeOrderReceived["receivedStatus"], ChangeOrderReceived["changeOrderID"]))
        g.appdb.commit()
        newID = ChangeOrderReceived["changeOrderID"]

        for i in ChangeOrderReceived["receivedChangeOrder"]:
            if i["receivedAmount"] == 0 and i["currencyId"] > 0:
                delete = """ DELETE from change_order_details where id = %s """
                cursor.execute(delete, (i["currencyId"], ))
                g.appdb.commit()

            elif i["currencyId"] > 0:
                update = """ UPDATE change_order_details set received_amount = %s where id = %s """
                cursor.execute(update, (i["receivedAmount"], i["currencyId"]))
                g.appdb.commit()

            elif i["currencyId"] == 0:
                insert = """ INSERT INTO change_order_details (change_order_id, currency_id, received_amount) VALUES (%s, %s, %s) """
                cursor.execute(insert, (newID, i["currency"], i['receivedAmount']))
                g.appdb.commit()

        logger.info('Exited from ChangeOrderReceived post method')
        return jsonify({"status":"success", "response":newID})
