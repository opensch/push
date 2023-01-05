from datetime import datetime
from flask import Flask, request
import requests
import hashlib
import config as config
import json

app = Flask(__name__)

def sendFirebase(token, title, content):
		data = {
				"to": token,
				"notification": {
						"title": title,
						"body": content
				}
		}
		requests.post("https://fcm.googleapis.com/fcm/send", headers = {"Content-Type": "application/json", "Authorization": "key="+config.googleFCM}, data = json.dumps(data))

def signature(pushToken, username, title, body, time):
	# create sha256 signature 
	signature = hashlib.sha256()
	signature.update(pushToken+username+title+body+time)
	return signature.hexdigest()

@app.route('/')
def pushServer():
	return ''

@app.route('/push', methods=['POST'])
def push():
	'''
		Parameters:
			pushToken: Token of the device
			schoolAPI: API of the school
			title: Title of the message
			body: body of the message
			signature: SHA256 signature of pushToken, username, text and time
	
	'''
	data = json.loads(request.data)
	
	if not "pushToken" in data or not "username" in data or not "schoolAPI" in data or not "title" in data or not "body" in data or not "time" in data or not "signature" in data:
		return "Missing parameters", 400

	if config.requireSignature != True:
		sendFirebase(data["pushToken"], data["title"], data["body"])
		return "OK", 200
	
	currentHour = datetime.now().hour
	currentMinute = datetime.now().minute
	time = currentHour + currentMinute

	# get username from schoolAPI
	url = "https://"+data["schoolAPI"]+"/pushSignature"
	r = requests.get(url)

	if r.status_code != 200:
		return "Can't verify signature", 500

	username = r.text
	if data['signature'] != signature(data['pushToken'], username, data['title'], data['body'], data['time']):
		return "Invalid signature", 403

	sendFirebase(data["pushToken"], data["title"], data["body"])


app.run()