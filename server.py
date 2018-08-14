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
		results = searcher.search(query)
		print("\nLength of results: " + str(len(results)) + '\n')
		result=[[],[],[],[]]
		for line in results:
			result[0].append(str(line['Access_Name']))
			result[1].append(str(line['County']))
			result[2].append(str(line['Type']))
			result[3].append(str(line['Location']))
		return result

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	print("Someone is at the home page.")
	return render_template('welcome_page.html')

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
	return render_template('results.html', query=query2, results=zip(result[0], result[1], result[2], result[3]))

if __name__ == '__main__':
	app.run(debug=True)
