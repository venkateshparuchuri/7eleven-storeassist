#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, g
from flask_restful import reqparse
from flask_restful import Resource, Api
import kaptan
import os
import MySQLdb
import logging
import json
import logging.config
import sys
from MySQLdb import cursors

from routes.auth import UserLogin
from routes.auth import AddUser
from routes.auth import AddUserStoresList
from routes.check import CardCheckReport
from routes.check import ItEquipmentReport
from routes.check import ChangeOrder
from routes.check import ChangeOrderHistory
from routes.check import ChangeOrderReceived
from routes.bakery import BakeryOrders
from routes.bakery import Message
from routes.bakery import ManualGasDipReport
from routes.bakery import DipReportByDate
from routes.shelfTag import ShelfTag
from routes.moneyOrder import MoneyOrderInquire
from routes.moneyOrder import MoneyOrderCash

app = Flask(__name__)

config = kaptan.Kaptan(handler="json")
config.import_config(os.getenv("CONFIG_FILE_PATH", 'config.json'))
environment = config.get('environment')

api = Api(app)
logger = logging.getLogger(__name__)

def connect_db():
    """Connects to the specific database."""
    try:
        db = MySQLdb.connect(host=config.get('dbhost'),  # your host, usually localhost
                         user=config.get("dbuser"),  # your username
                         passwd=config.get("dbpass"),  # your password
                         db=config.get("dbname"), cursorclass=MySQLdb.cursors.DictCursor,sql_mode="STRICT_TRANS_TABLES")  # name of the data base
        return db
    except:
        logger.error('Failed to Connect to the database', exc_info=True)
        sys.exit("not able to connect to database")

def connect_2():
    """Connects to the specific database."""
    try:
        db2 = MySQLdb.connect(host=config.get('bakerydbhost'),  # your host, usually localhost
                        user=config.get("bakerydbuser"),  # your username
                        passwd=config.get("bakerydbpass"),  # your password
                        db=config.get("bakerydbname"), cursorclass=MySQLdb.cursors.DictCursor,sql_mode="STRICT_TRANS_TABLES")  # name of the data base
        return db2
    except:
        logger.error('Failed to Connect to the database', exc_info=True)
        sys.exit("not able to connect to database")

def connect_message():
    """Connects to the specific database."""
    try:
        db_message = MySQLdb.connect(host=config.get('messagedbhost'),  # your host, usually localhost
                        user=config.get("messagedbuser"),  # your username
                        passwd=config.get("messagedbpass"),  # your password
                        db=config.get("messagedbname"), cursorclass=MySQLdb.cursors.DictCursor,sql_mode="STRICT_TRANS_TABLES")  # name of the data base
        return db_message
    except:
        logger.error('Failed to Connect to the database', exc_info=True)
        sys.exit("not able to connect to database")

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'appdb'):
        g.appdb = connect_db()
    return g.appdb

def get_another_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'appdbNew'):
        g.appdbNew = connect_2()
    return g.appdbNew

def get_message_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'messagedb'):
        g.messagedb = connect_message()
    return g.messagedb


@app.before_request
def before_request():
    g.appdb = get_db()
    g.appdbNew = get_another_db()
    g.messagedb = get_message_db()
    setEmailRequirements()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'appdb'):
        g.appdb.close()
    if hasattr(g,'appdbNew'):
        g.appdbNew.close()
    if hasattr(g,'messagedb'):
        g.messagedb.close()


@app.before_first_request
def setup_logging(default_path='logconf.json', default_level=logging.INFO, env_key='LOG_CFG_PATH'):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def setEmailRequirements():
    if not hasattr(g, 'config'):
        g.config = config
    g.moneyorder_server = config.get("moneyorder_server")
    g.moneyorder_db = config.get("moneyorder_db")
    g.moneyorder_user = config.get("moneyorder_user")
    g.moneyorder_password = config.get("moneyorder_password")

api.add_resource(UserLogin, '/api/route/auth/login', endpoint = 'auth')
api.add_resource(AddUser, '/api/route/auth/addUser', endpoint='adduser')
api.add_resource(AddUserStoresList, '/api/route/auth/addUserStoresList', endpoint='addUserStoresList')
api.add_resource(CardCheckReport, '/api/route/check/cardCheckReport', endpoint = 'cardCheckReport')
api.add_resource(ItEquipmentReport, '/api/route/check/itEquipmentReport', endpoint = 'itEquipmentReport')
api.add_resource(ChangeOrder, '/api/route/check/changeOrder', endpoint = 'changeOrder')
api.add_resource(ChangeOrderHistory, '/api/route/check/changeOrderHistory', endpoint = 'changeOrderHistory')
api.add_resource(ChangeOrderReceived, '/api/route/check/changeOrderReceived', endpoint = 'changeOrderReceived')
api.add_resource(BakeryOrders, '/api/route/bakery/bakeryOrders', endpoint = 'bakeryOrders')
api.add_resource(Message, '/api/route/bakery/message', endpoint = 'message')
api.add_resource(ManualGasDipReport, '/api/route/bakery/manualGasDipReport', endpoint = 'manualGasDipReport')
api.add_resource(DipReportByDate, '/api/route/bakery/dipReportByDate', endpoint = 'dipReportByDate')
api.add_resource(ShelfTag, '/api/route/bakery/shelfTag', endpoint = 'shelfTag')
api.add_resource(MoneyOrderInquire, '/api/route/moneyOrder/moneyOrderInquire', endpoint = 'moneyOrderInquire')
api.add_resource(MoneyOrderCash, '/api/route/moneyOrder/moneyOrderCash', endpoint = 'moneyOrderCash')

@app.route('/api')
def index():
    # same result even with Flask-MySQL - We need to use the Index to Get
    # Values and Map to OrderedDict to create JSON.

    logger.info('Entered into Get /api Call')
    logger.debug(request.headers.get('User-Agent'))
    logger.info('Exiting from Get /api Call')
    return jsonify({"status": "success", "response": "API is up at the URL", "fetched": rv})

#,ssl_context='adhoc'
if __name__ == '__main__':
    app.run(host=config.get("host"), debug=config.get("debug"))
