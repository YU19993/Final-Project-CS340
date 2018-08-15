from flask import Flask, render_template, url_for, request
import sys
import whoosh
import os
import shutil
import os.path
from whoosh.index import open_dir
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
import numpy  as np
import pandas as pd
import string

def search(indexer, searchTerm, searchColumns):
	with indexer.searcher() as searcher:
		words = searchColumns
		query = MultifieldParser(words, schema=indexer.schema).parse(searchTerm)
		results = searcher.search(query, limit=None)
		print("\nLength of results: " + str(len(results)) + '\n')
		result=[[],[],[],[]]
		for line in results:
			result[0].append(str(line['Access_Name']))
			result[1].append(str(line['County']))
			result[2].append(str(line['Type']))
			result[3].append(str(line['Location']))
		return result

def searchh(indexer, searchTerm):
	with indexer.searcher() as searcher:
		words = ['Access_Name']
		query = MultifieldParser(words, schema=indexer.schema).parse(searchTerm)
		results = searcher.search(query)
		print("\nLength of results: " + str(len(results)) + '\n')
		result = []
		scm = ['Access_Name', 'URL', 'imgURL', 'County', 'Type', 'Location', 'Access_Type', 'Path_to_Beach', 'Managed_by']
		scm = scm + ['Parking', 'Fee', 'Bathrooms', 'Handicap_Access', 'Running_Water', 'Showers', 'Camp_Sites', 'Stairs_to_Beach', 'Boat_Ramps', 'Tidepooling']
		scm = scm + ['Surfing', 'Hiking', 'Bicycling', 'Horseback_Riding', 'Road_Vehicle_Access', 'Whale_Watching']
		if(len(results)>0):
			for x in scm:
				result.append(results[0][x])

		return result


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	print("Someone is at the home page.")
	return render_template('welcome_page.html')

@app.route('/about/', methods=['GET', 'POST'])
def about():
	return render_template('about.html')

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
	return render_template('contact.html')

@app.route('/my-link/')
def my_link():
	print('I got clicked!')
	return 'Click.'

@app.route('/results/', methods=['GET', 'POST'])
def results():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	query1 = data.get('searchterm')
	query2 = data.get('searchitem')
	print("\nYou searched for: " + str(query1)+'\n')
	print("\nYou searched for: " + str(query2)+'\n')
	searchTerm = str(query2)
	searchColumns = []
	searchColumns.append(str(query1))
	dx = open_dir("indexdir")		#keep data in local folder
	result = search(dx, searchTerm, searchColumns)
	for x in result:
		print(x)
	if(len(result[0]) == 0):
		return render_template('not_found.html')
	else:
		return render_template('results.html', query=query2, results=zip(result[0], result[1], result[2], result[3]))


@app.route('/detial/', methods=['GET', 'POST'])
def detial():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args
	dx = open_dir("indexdir")
	query = data.get('More_Detial')
	print("\nMore Detial for: " + str(query)+'\n')
	result = searchh(dx,str(query))
	print(result)
	print("\nThis page privide more detial about the search.\n")
	return render_template('detial.html', r0=result[0], r3=result[3], r4=result[4], r5=result[5], r6=result[6], r7=result[7],r8=result[8], r9=result[9], r10=result[10],r11=result[11], r12=result[12], r13=result[13], r14=result[14], r15=result[15], r16=result[16], r17=result[17], r18=result[18], r19=result[19], r20=result[20], r21=result[21], r22=result[22], r23=result[23],r24=result[24])
	#return render_template('detial.html')
if __name__ == '__main__':
	app.run(debug=True)
