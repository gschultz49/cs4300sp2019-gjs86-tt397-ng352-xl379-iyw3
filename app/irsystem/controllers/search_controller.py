from . import *  
from app.irsystem.models.helpers import *

from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from app.irsystem.models.search import *


# The actual IR system that will take the [query] and return the results as an array of objects
def ir_retrieve(query):
	print ("THE QUERY: {0}".format(query))
	results = FindSimilarShoes(query)
	print (results)
	return results

# JUST FOR DEMO
def fuzzy(query):
	print("THE QUERY: {0}".format(query))
	results = FindQuery(query)
	print(results)
	return results
	
# used for ajax retrieval
@irsystem.route('/retrieve')
def retrieve():
	query = request.args.get('search')
	# need to json.dumps the array for .getJSON to work
	results = json.dumps(ir_retrieve(query))
	return results
	
@irsystem.route('/splash', methods=['GET'])
def splash():
	# pick default shoe?
	return render_template('splash.html', 
	data=ir_retrieve("Nike Air Zoom Pegasus 35")
	)

@irsystem.route('/fuzzy', methods=['GET'])
def fuzzy_page():
	# pick default shoe?
	return render_template('splash.html', 
	data=fuzzy("cool") 
	)
