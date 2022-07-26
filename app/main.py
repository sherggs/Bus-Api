from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import hashlib
import datetime
import mysql.connector

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

@app.route('/')
def index():
    return "up and running :)"

class SignUp(Resource):
    def post(self):
        try:
            data = request.data
            data = json.loads(data)

            mydb = mysql.connector.connect(
                host="divinechristianassembly.com",
                user="u505151495_digibus",
                database="u505151495_digibus",
                password="Iaamfsd,gu2i",
            )
            cursor = mydb.cursor()

            sql = "SELECT * FROM users WHERE email='{}'".format(data['email'])
            cursor.execute(sql)
            result = cursor.fetchone()
            if result != None:
                return {"error": True, "msg": 'Email address is taken'}
            sql = "SELECT COUNT(*) FROM users "
            cursor.execute(sql)
            result = cursor.fetchone()
            userID = "TD-U-{:04d}".format(result[0] + 1)
            password = hashlib.sha256(data['password'].encode()).hexdigest()
            dateJoined = datetime.datetime.now().strftime("%d %b, %Y")
            sql = "INSERT INTO users (userID, fullName, email, password, walletBalance, dateJoined) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (userID, data['fullName'],
                data['email'], password, 0, dateJoined)
            cursor.execute(sql, val)
            mydb.commit()
            return {"error": False, "msg": "Created User Successfully", 'userID': userID}

        except Exception as e:
            return {"error": True, "msg": str(e)}


class Login(Resource):
    def post(self):
        try:
            data = request.data
            data = json.loads(data)

            mydb = mysql.connector.connect(
                host="divinechristianassembly.com",
                user="u505151495_digibus",
                database="u505151495_digibus",
                password="Iaamfsd,gu2i",
            )
            cursor = mydb.cursor()
            password = hashlib.sha256(data['password'].encode()).hexdigest()
            sql = "SELECT * FROM users WHERE email='{}' AND password='{}'".format(
                data['email'], password)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result == None:
                return {"error": True, "msg": 'Invalid login details'}
            user = {
                'userID': result[0],
                'fullName': result[1],
                'email': result[2],
                'walletBalance': result[4],
            }
            return {"error": False, "msg": "Logged in sucessfully", 'user': user}

        except Exception as e:
            return {"error": True, "msg": str(e)}
