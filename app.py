# -*- coding: utf-8 -*-
import os, datetime
import re
from unidecode import unidecode


from flask import Flask, request, render_template, redirect, abort

# import all of mongoengine
from mongoengine import *

# import data models
import models

# for json needs
import json
from flask import jsonify


from collections import Counter

import requests

app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = False


@app.route('/')
def get_remote_ideas():

	# ideas available via json
	mail_url = "http://itpmailcall.herokuapp.com/data/mailpieces/onshelf"
	meal_url = "http://www.hungryfr.com/data/json"

	# make a GET request to the url
	mail_request = requests.get(mail_url)
	meal_request = requests.get(meal_url)

	# log out what we got
	# app.logger.info(mail_request.json)
	# app.logger.info(meal_request.json)

	# requests will automatically convert json for us.
	# .json will convert incoming json to Python dictionary for us
	mail_data = mail_request.json
	meal_data = meal_request.json

	# alternative way
	# ideas_data = json.loads( idea_request.text )

	# the returned json looks like
	# {
	# 	'status' : 'OK',
	# 	'ideas' : [
	# 		{
	# 		timestamp: "2012-10-02 09:16:54.086000",
	# 		title: "Immortality",
	# 		idea: "Immortality is the ability to live forever, or put another way, it is an immunity from death. It is unknown whether human physical (material) immortality is an achievable condition.",
	# 		comments: [ ],
	# 		creator: "John"
	# 		},
	# 		...
	# 	]
	# }

	# app.logger.info(mail_data.get('ideas'))
	# app.logger.info(mail_data.get('ideas').to)
	
	# for i in mail_data['ideas']:
	# 	app.logger.info(i['to'])

	mailnames=[]
	mealnames=[]
	matches=[]
	vendors=[]
	

	for i in mail_data['ideas']:
		mailnames.append(i['to']);		
	
	for j in meal_data['ideas']:
		mealnames.append(j['creator']);		


	for m in mealnames:
		for n in mailnames:
			if m == n:
				matches.append(m);


	for i in mail_data['ideas']:
		vendors.append(i['from']);		

	cnt = Counter()
	for word in vendors:
		cnt[word] += 1

	# app.logger.info(cnt.values())
	maxvendor=max(cnt, key=cnt.get)



	if mail_data.get('status') == "OK" and meal_data.get('status') == "OK" :
		templateData = {
			'matches' : matches,
			'maxvendor' : maxvendor
		}

		return render_template('remote_ideas.html', **templateData)

	
	else:
		return "uhoh something went wrong - status = %s" % ideas_data.get('status')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# slugify the title 
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))



# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	