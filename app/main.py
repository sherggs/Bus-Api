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
                host="localhost:8080",
                user="root",
                database="theDigitalBus",
                password="",
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

class GetAllUsers(Resource):
    def get(self):
        try:
            mydb = mysql.connector.connect(
                host="divinechristianassembly.com",
                user="u505151495_digibus",
                database="u505151495_digibus",
                password="Iaamfsd,gu2i",
            )
            cursor = mydb.cursor()
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result == None:
                return {"error": True, "msg": 'No user'}
            users = []
            for user in result:
                userData = {
                    'userID': user[0],
                    'fullName': user[1],
                    'email': user[2],
                    'walletBalance': user[4],
                    'dateJoined': user[5],
                }
                users.append(userData)
            users.reverse()
            return {"error": False, "users": users}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
class CreateTrip(Resource):
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

            sql = "SELECT COUNT(*) FROM trips "
            cursor.execute(sql)
            result = cursor.fetchone()
            tripID = "TD-T-{:04d}".format(result[0] + 1)
            dateCreated = datetime.datetime.now().strftime("%d %b, %Y")
            sql = "INSERT INTO trips (tripID, origin, destination, price, time, dateCreated) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (tripID, data['origin'],
                data['destination'], data['price'], data['time'], dateCreated)
            cursor.execute(sql, val)
            mydb.commit()
            return {"error": False, "msg": "Created Trip Successfully, Enjoy your Journey", "tripID": tripID}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
        
class GetAllTrips(Resource):
    def get(self):
        try:
            mydb = mysql.connector.connect(
                host="divinechristianassembly.com",
                user="u505151495_digibus",
                database="u505151495_digibus",
                password="Iaamfsd,gu2i",
            )
            cursor = mydb.cursor()
            sql = "SELECT * FROM trips"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result == None:
                return {"error": True, "msg": 'No trip'}
            trips = []
            for trip in result:
                tripData = {
                    'tripID': trip[0],
                    'origin': trip[1],
                    'destination': trip[2],
                    'price': trip[3],
                    'time': trip[4],
                    'dateCreated': trip[5],
                }
                trips.append(tripData)
            trips.reverse()
            return {"error": False, "trips": trips}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
