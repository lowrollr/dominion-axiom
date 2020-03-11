from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

@app.route('/highScores', methods=['GET'])
def getHighScores(self):
    conn = db_connect.connect() # connect to database
    query = conn.execute("SELECT * FROM users ORDER BY score DESC LIMIT 10") # This line performs query and returns json result
    return {'users': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

if __name__ == '__main__':
     app.run(debug=True, port='5002')