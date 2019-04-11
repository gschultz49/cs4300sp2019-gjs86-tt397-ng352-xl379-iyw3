from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *

# The actual IR system that will take the [query] and return the results as an array of objects
def ir_retrieve(query):
	print ("THE QUERY: {0}".format(query))
	results = [
		{
			"shoeName": "Nike Air Zoom Pegasus 35",
			"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg",
			"similarityScore": 0.5,
			"relevantTerms": ["soft", "warm"],
			"corescore": 95,
			"similarShoes": ["Nike Air Zoom Pegasus 40", "Nike Air Zoom Pegasus 34"]
		},
		{
			"shoeName": "Nike Air Zoom Pegasus 35",
			"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg",
			"similarityScore": 0.5,
			"relevantTerms": ["soft", "warm"],
			"corescore": 95,
			"similarShoes": ["Nike Air Zoom Pegasus 40", "Nike Air Zoom Pegasus 34"]
		},
		{
			"shoeName": "Nike Air Zoom Pegasus 35",
			"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg",
			"similarityScore": 0.5,
			"relevantTerms": ["soft", "warm"],
			"corescore": 95,
			"similarShoes": ["Nike Air Zoom Pegasus 40", "Nike Air Zoom Pegasus 34"]
		}
	]

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
	return render_template('splash.html', data=ir_retrieve("Nike Air Zoom Pegasus 35"))





# project_name = "TEAM SOLEMATE"
# net_id = "dnm"
# @irsystem.route('/', methods=['GET'])
# def search():
# 	query = request.args.get('search')
# 	netIDS = [
# 		"gjs86",
# 		"tt397",
# 		"ng352",
# 		"xl379",
# 		"iyw3"
# 	]
# 	if not query:
# 		data = []
# 		output_message = ''
# 	else:
# 		output_message = "Your search: " + query
# 		data = range(5)
# 	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, netIDS = netIDS)
