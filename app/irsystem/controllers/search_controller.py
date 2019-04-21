from . import *  
# from app.irsystem.models.helpers import *	
# from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from app.irsystem.models.search import *

# used for ajax retrieval
@irsystem.route('/custom_search')
def custom_search():
	query = request.args.get('search')
	print (query)
	# need to json.dumps the array for .getJSON to work
	results = json.dumps(FindSimilarShoes(query))
	print (results)
	return results


@irsystem.route('/', methods=['GET'])
def index():
	return render_template('index.html')


# # The actual IR system that will take the [query] and return the results as an array of objects
# def ir_retrieve(query):
# 	print ("THE QUERY: {0}".format(query))
# 	results = FindSimilarShoes(query)
# 	print (results)
# 	return results

# # used for ajax retrieval
# @irsystem.route('/retrieve')
# def retrieve():
# 	query = request.args.get('search')
# 	# need to json.dumps the array for .getJSON to work
# 	results = json.dumps(ir_retrieve(query))
# 	return results

# @irsystem.route('/splash', methods=['GET'])
# def splash():
# 	# pick default shoe?
# 	return render_template('splash.html',
# 		data=ir_retrieve("Nike Air Zoom Pegasus 35")
# 	)

# # JUST FOR DEMO
# def ir_fuzzy(query):
# 	print("THE QUERY: {0}".format(query))
# 	results = FindQuery(query)
# 	print(results)
# 	return results
	
# # JUST FOR DEMO
# @irsystem.route('/retrieve_fuzzy')
# def retrieve_fuzzy():
# 	query = request.args.get('search')
# 	# need to json.dumps the array for .getJSON to work
# 	results = json.dumps(ir_fuzzy(query))
# 	return results

# # JUST FOR DEMO
# @irsystem.route('/fuzzy', methods=['GET'])
# def fuzzy_page():
# 	# pick default shoe?
# 	return render_template('fuzzy.html', 
# 	data=ir_fuzzy("cool")
# 	)
