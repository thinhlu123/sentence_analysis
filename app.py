from flask import Flask, render_template, request,jsonify
import json
from sentence_analysis import separateEntity

app = Flask(__name__)
separate = separateEntity()

def check_WH(data):
	res = separate.checkWHQuestion(data)
	return res

def analysis_sen(data):
	res = {}
	res["type"] = separate.checkWHQuestion(data)
	res["title"] = separate.getTitle(data)
	res["object"] = separate.getObject(data)
	res["action"] = separate.getAction(data)
	return res

# Truyen vao body "sentence":"abc"
@app.route("/check-wh-question", methods=["POST"])
def checkWH():
	data = request.get_json()
	res = check_WH(data['sentence'])
	return jsonify(resp = res)

@app.route("/analysis-sentence", methods=["POST"])
def analysis():
	data = request.get_json()
	res = analysis_sen(data['sentence'])
	print(data['sentence'])
	return jsonify(resp = res)

if __name__ == "__main__":
    #app.run( host='172.29.64.182', port=274, debug = True, ssl_context="adhoc")
	app.run()

