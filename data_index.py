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
		print("Length of results: " + str(len(results)))
		result=[[],[],[],[]]
		for line in results:
			result[0].append(line['Access_Name'])
			result[1].append(line['County'])
			result[2].append(line['Type'])
			result[3].append(line['Location'])
		return result

def index():

	if(os.path.isdir("indexdir")):
		shutil.rmtree("indexdir", ignore_errors=True)
	os.mkdir("indexdir")

	scm = ['Access_Name', 'URL', 'imgURL', 'County', 'Type', 'Location', 'Access_Type', 'Path_to_Beach', 'Managed_by']
	scm = scm + ['Parking', 'Fee', 'Bathrooms', 'Handicap_Access', 'Running_Water', 'Showers', 'Camp_Sites', 'Stairs_to_Beach', 'Boat_Ramps', 'Tidepooling']
	scm = scm + ['Surfing', 'Hiking', 'Bicycling', 'Horseback_Riding', 'Road_Vehicle_Access', 'Whale_Watching']

	schema = Schema()
	indexer = create_in("indexDir", schema)

	data = pd.read_csv('beach_access_data.csv')
	ele_name = data.columns.tolist()

	ds = []
	for x in range(len(scm)):
		ds.append([])

	for x in range(len(data.index)):
		for xx in range(len(ds)):
			ds[xx].append(str(data[ele_name[xx]][x]))

	writer = indexer.writer()

	for x in range(len(scm)):
		writer.add_field(scm[x], TEXT(stored=True))

	for x in range(len(ds[0])):
		writer.add_document(Access_Name=ds[0][x], URL=ds[1][x], imgURL=ds[2][x], County=ds[3][x], Type=ds[4][x], Location=ds[5][x], Access_Type=ds[6][x], Path_to_Beach=ds[7][x], Managed_by=ds[8][x], Parking=ds[9][x], Fee=ds[10][x], Bathrooms=ds[11][x], Handicap_Access=ds[12][x], Running_Water=ds[13][x], Showers=ds[14][x], Camp_Sites=ds[15][x], Stairs_to_Beach=ds[16][x], Boat_Ramps=ds[17][x], Tidepooling=ds[18][x], Surfing=ds[19][x], Hiking=ds[20][x], Bicycling=ds[21][x], Horseback_Riding=ds[22][x], Road_Vehicle_Access=ds[23][x], Whale_Watching=ds[24][x])

	writer.commit()
	return indexer

def main():
	searchTerm = 'Fort Stevens And Park'
	dx = index()
	searchColumns = ["Access_Name", "URL"]		#search attributions
	#dx = open_dir("indexdir")		#keep data in local folder
	results = search(dx, searchTerm, searchColumns)
	for x in results:
		print(x)



if __name__ == '__main__':
	main()
