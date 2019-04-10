from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

# The actual IR system that will take the [query] and return the results as an array of objects
def ir_retrieve(query):
	print ("THE QUERY: {0}".format(query))
	results =[
		{
				"shoeName": "Nike Air Zoom Pegasus 35",
				"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg",
					"shoeURL": "https://runrepeat.com/nike-air-zoom-pegasus-35"
		},
			{
				"shoeName": "Nike Epic React Flyknit",
					"shoeImage": "https://cdn.runrepeat.com/i/nike/27379/nike-men-s-epic-react-flyknit-running-shoes-11-5-grey-white-mens-grey-white-aad2-main.jpg",
					"shoeURL": "https://runrepeat.com/nike-epic-react-flyknit"
		},
		# random filler for grid testing
		{"shoeName": "Nike Air Zoom Pegasus 35", "shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg", "shoeURL": "https://runrepeat.com/nike-air-zoom-pegasus-35"}, {"shoeName": "Nike Air Zoom Pegasus 35", "shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg", "shoeURL": "https://runrepeat.com/nike-air-zoom-pegasus-35"}, {"shoeName": "Nike Air Zoom Pegasus 35", "shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg", "shoeURL": "https://runrepeat.com/nike-air-zoom-pegasus-35"}]
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
	e = [1, 'foo']
	return render_template('splash.html', bleh = json.dumps(e), data=ir_retrieve("Nike Air Zoom Pegasus 35"))







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
