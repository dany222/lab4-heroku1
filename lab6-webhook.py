from flask import Flask,jsonify,request,send_from_directory
import sqlite3
import os
#import requests

app = Flask(__name__)

#dbfunctions
def initDatabase():
	conn = sqlite3.connect('about.db')
	cur = conn.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS person(id INTEGER PRIMARY KEY, name VARCHAR(100), age INTEGER)')
	conn.commit()

def fetchDataFromDatabase():
	with sqlite3.connect('about.db') as conn:
		cur = conn.cursor()
		result = cur.execute("SELECT * FROM person ORDER BY id DESC;").fetchone()
		return jsonify(id = result[0],name = result[1], age = result[2])

def pushDataToDatabase(name,age):
	with sqlite3.connect('about.db') as conn:
		cur = conn.cursor()
		sql = f"INSERT INTO person (name,age) VALUES ('{name}',{age});"
		cur.execute(sql)
		conn.commit()


static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')


# @app.route("/api/bot",methods = ['POST'])
# def hook():
# 	webhookMessage = request.json
# 	print(webhookMessage)
# 	messageId = webhookMessage["data"]["id"]
# 	print(messageId)
# 	# url = "https://api.ciscospark.com/v1/messages/" + messageId
# 	# r = requests.get(url,headers={'Authorization' : 'Bearer ZGZkNTQ2Y2YtMzVjYi00NzE0LWJjMjMtNzQ4YTA0Y2I3YWY3ZWUzMjQ4MjEtZGI3_PF84_consumer'})
# 	# message = r.json()["text"]
# 	# print(message)
# 	return jsonify(webhookMessage)

@app.route("/<path:path>",methods = ['GET'])
def serve_static_dir(path):
	return send_from_directory(static_file_dir,path)

@app.route("/")
def index():
	return app.send_static_file('index.html')

@app.route("/api/helloworld")
def hello():
	return("Hello World!")

name = "John"
age = 17
@app.route("/api/about", methods = ['POST','GET'])
def about():
	if request.method == 'GET':
		return fetchDataFromDatabase()
	elif request.method == 'POST':
		name = request.json["name"]
		age = request.json["age"]                     
		pushDataToDatabase(name,age)
		return jsonify(name = name, age = age)



initDatabase()
pushDataToDatabase('Charles Webex', 17)

if __name__ == "__main__":
	app.run()
    