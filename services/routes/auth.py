from flask_restful import reqparse
from flask_restful import Resource
from flask import  jsonify, abort, make_response, request, g
import MySQLdb
import collections
import logging
import hashlib, uuid

from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from jsonschema import validate

UserLoginSchema = {
    'type': 'object',
    'properties': {
        'userid': {'type': 'string'},
		'password': {'type': 'string'}
    },
	"required": ["password","userid"]
}

class UserLoginSchemaApiInputs(Inputs):
    json = [JsonSchema(schema=UserLoginSchema)]

class UserLogin(Resource):
    def post(self):
        logger = logging.getLogger("UserLogin post")
        logger.info('Entered into UserLogin method')

        inputs = UserLoginSchemaApiInputs(request)
        if not inputs.validate():
            return jsonify(success=False, errors=inputs.errors)

        try:
            user = request.json
            cursor = g.appdb.cursor()
            username = user["userid"]
            password = user["password"]
        except:
            logger.error("variables from url", exc_info=True)
        qury = """ SELECT password FROM user where user_id = %s """
        cursor.execute(qury,(username,))

        saltciphertext = cursor.fetchone()
        salt = saltciphertext["password"][0:32]
        cipher_db = saltciphertext["password"][32:]
        cipher_front = hashlib.sha256(password + salt).hexdigest()

        query = """ SELECT u.id, u.user_id as user_id, u.email, r.name as role, s.name as store_name, u.name as username, s.id as store_id
              FROM user u
              inner join user_role ur on u.id = ur.user_id
              inner join role r on ur.role_id = r.id
              left outer join store s on s.id = ur.store_id
              where BINARY u.user_id = %s and BINARY u.password = %s """
        cursor.execute(query,(username, salt + cipher_front))
        rv = cursor.fetchall()

        return jsonify({"status":"success","response":rv})

class AddUser(Resource):

    def post(self):
        logger = logging.getLogger("Add_user")
        logger.info('Entered into Add_user  post method')
        try:
            value = request.json
            user_id = value["user_id"]
            name = value["name"]
            email = value["email"]
            password = value["password"]
            initials = value["initials"]
            role_id = value["role_id"]
            store_id = value["store_id"]

            salt = uuid.uuid4().hex
            cipher = hashlib.sha256(password+salt).hexdigest()
            pass_db = salt+cipher
            cursor = g.appdb.cursor()

        except:
            logger.error("DB connection or url parameters error", exc_info=True)
        query = """ INSERT INTO user (user_id, name, email, password, initials) VALUES (%s, %s, %s, %s, %s) """
        query_2 = """ INSERT INTO user_role (user_id, role_id, store_id) VALUES (%s, %s, %s) """
        cursor.execute(query,(user_id, name, email, pass_db, initials))
        g.appdb.commit()
        newID = cursor.lastrowid
        cursor.execute(query_2,(newID, role_id, store_id))
        g.appdb.commit()

        logger.info('Exited from Add_User post method')
        return jsonify({"status":"success", "response":"New user created successfully"})

    def get(self):
        logger = logging.getLogger("UserRole get")
        logger.info('Entered into UserRole get method')

        try:
            cursor = g.appdb.cursor()
            store_id = request.values.get("store_id")
        except:
            logger.error('DB Connection error', exc_info=True)

        query = """ SELECT r.id, r.name from role r where r.name not in ('Admin')
              and r.id not in (select ur.role_id from user_role ur where ur.store_id = %s) """
        cursor.execute(query, (store_id,))
        rv = cursor.fetchall()

        logger.info('Exited from UserRole get method')
        return jsonify({"status":"success", "response":rv})

class AddUserStoresList(Resource):
    def get(self):
        logger = logging.getLogger("AddUserStoresList get")
        logger.info('Entered into AddUserStoresList  get method')

        try:
            cursor = g.appdb.cursor()
        except:
            logger.error('DB Connection error', exc_info=True)
        query = """ SELECT id AS store_id from store where id not in (
              select store_id from user_role ur
              inner join role r on ur.role_id = r.id
              where r.name in ('Employee', 'Manager')
              group by store_id having count(*)>=2) """
        cursor.execute(query)
        rv = cursor.fetchall()
        
        logger.info('Exited from AddUserStoresList Get method')
        return jsonify({"status":"success", "response":rv})
