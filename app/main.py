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
    return "up and running  for the database :)"

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
            userID = "DG-U-{:04d}".format(result[0] + 1)
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
            tripID = "DG-T-{:04d}".format(result[0] + 1)
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
        
class GetTrip(Resource):
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
            sql = "SELECT * FROM trips WHERE tripID = '{}'".format(
                data['tripID'])
            cursor.execute(sql)
            result = cursor.fetchone()
            if result == None:
                return {"error": True, "msg": 'Trip Does Not Exist'}
            trip = {
                'tripID': result[0],
                'origin': result[1],
                'destination': result[2],
                'price': result[3],
                'time': result[4],
                'dateCreated': result[5],
            }
            return {"error": False, "trip": trip}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
        
class UpdateTrip(Resource):
    def put(self):
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
            sql = "UPDATE trips SET origin = %s, destination = %s, price = %s, time = %s WHERE tripID = %s"
            val = (data['origin'],
                data['destination'], data['price'], data['time'], data['tripID'])

            cursor.execute(sql, val)
            mydb.commit()
            return {"error": False, "msg": "Updated Trip Successfully"}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
class DeleteTrip(Resource):
    def delete(self):
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
            sql = "DELETE FROM trips WHERE tripID = '{}'".format(
                data['tripID'])
            cursor.execute(sql)
            mydb.commit()
            return {"error": False, "msg": 'Deleted Trip Successfully'}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
class CreateBooking(Resource):
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

            sql = "INSERT INTO bookings (tripID, userID, fullName, tripName, amountPaid, tripTime, dateOfTrip) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (data['tripID'], data['userID'], data['fullName'], data['tripName'],
                data['amountPaid'], data['tripTime'], data['dateOfTrip'])
            cursor.execute(sql, val)
            mydb.commit()
            return {"error": False, "msg": "Created Booking Successfully"}

        except Exception as e:
            return {"error": True, "msg": str(e)}

class GetAllBookings(Resource):
    def get(self):
        try:
            mydb = mysql.connector.connect(
                host="divinechristianassembly.com",
                user="u505151495_digibus",
                database="u505151495_digibus",
                password="Iaamfsd,gu2i",
            )
            cursor = mydb.cursor()
            sql = "SELECT * FROM bookings"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result == None:
                return {"error": True, "msg": 'No Booking with that ID'}
            bookings = []
            for booking in result:
                bookingData = {
                    'tripID': booking[0],
                    'userID': booking[1],
                    'fullName': booking[2],
                    'tripName': booking[3],
                    'amountPaid': booking[4],
                    'tripTime': booking[5],
                    'dateOfTrip': booking[6],
                }
                bookings.append(bookingData)
            bookings.reverse()
            return {"error": False, "bookings": bookings}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
        
class GetBookings(Resource):
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
            sql = "SELECT * FROM bookings WHERE userID = '{}'".format(
                data['userID'])
            cursor.execute(sql)
            result = cursor.fetchall()
            if result == None:
                return {"error": True, "msg": 'No Booking with that ID'}
            bookings = []
            for booking in result:
                bookingData = {
                    'tripID': booking[0],
                    'userID': booking[1],
                    'fullName': booking[2],
                    'tripName': booking[3],
                    'amountPaid': booking[4],
                    'tripTime': booking[5],
                    'dateOfTrip': booking[6],

                }
                bookings.append(bookingData)
            bookings.reverse()
            return {"error": False, "trips": bookings}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
        
class DeleteBookings(Resource):
    def delete(self):
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
            sql = "DELETE FROM bookings WHERE userID = '{}'".format(
                data['userID'])
            cursor.execute(sql)
            mydb.commit()
            return {"error": False, "msg": 'Deleted Booking Successfully'}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
        
class FundWallet(Resource):
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
            sql = "SELECT walletBalance FROM users WHERE userID = '{}'".format(
                data['userID'])
            cursor.execute(sql)
            result = cursor.fetchone()
            if result == None:
                return {"error": True, "msg": 'User Does Not Exist'}
            balance = result[0]
            balance = int(balance) + int(data['amount'])
            sql = "UPDATE users SET walletBalance = %s WHERE userID = %s"
            val = (balance, data['userID'])
            cursor.execute(sql, val)
            mydb.commit()
            return {"error": False, "msg": 'Successfully Funded Wallet', 'balance': balance}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        
        
        
        
class GetMetrics(Resource):
    def get(self):
        try:

            mydb = mysql.connector.connect(
                host="divinechristianassembly.com",
                user="u505151495_digibus",
                database="u505151495_digibus",
                password="Iaamfsd,gu2i",
            )
            cursor = mydb.cursor()
            sql = "SELECT COUNT(*) FROM users "
            cursor.execute(sql)
            result = cursor.fetchone()
            users = result[0]
            sql = "SELECT COUNT(*) FROM trips "
            cursor.execute(sql)
            result = cursor.fetchone()
            trips = result[0]
            sql = "SELECT COUNT(*) FROM bookings "
            cursor.execute(sql)
            result = cursor.fetchone()
            bookings = result[0]
            metricData = {
                'users': users,
                'trips': trips,
                'bookings': bookings
            }
            return {"error": False, "metrics": metricData}

        except Exception as e:
            return {"error": True, "msg": str(e)}
        

api.add_resource(SignUp, '/signUp')
api.add_resource(Login, '/logIn')
api.add_resource(GetAllUsers, '/getAllUsers')
api.add_resource(CreateTrip, '/createTrip')
api.add_resource(GetAllTrips, '/getAllTrips')
api.add_resource(GetTrip, '/getTrip')
api.add_resource(UpdateTrip, '/updateTrip')
api.add_resource(DeleteTrip, '/deleteTrip')
api.add_resource(CreateBooking, '/createBooking')
api.add_resource(GetAllBookings, '/getAllBookings')
api.add_resource(GetBookings, '/getBookings')
api.add_resource(DeleteBookings, '/deleteBookings')
api.add_resource(GetMetrics, '/getMetrics')
api.add_resource(FundWallet, '/fundWallet')



if '__main__' == __name__:
    app.run(debug=True, port="3000")