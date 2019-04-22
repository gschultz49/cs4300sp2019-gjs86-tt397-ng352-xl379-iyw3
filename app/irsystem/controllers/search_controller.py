from . import *  
from app.irsystem.models.search import *

# helper, does searching
def _search (f, query):
	print (query)
	results = json.dumps(f(query['search'],query))
	print (results)
	return results

def _generate_dictionary (request, termlist, d={}):
	d = {}
	for t in termlist:
		if t in request.args:
			d[t] = request.args.get(t)
		else:
			d[t] = "N/A"
	return d

# used for ajax retrieval
@irsystem.route('/similar_search')
def similar_search():
	print ("IN SIMILAR SEARCH")
	return _search (FindSimilarShoes, request.args.get("search"))


# used for ajax retrieval
@irsystem.route('/custom_search')
def custom_search():
	print ("IN CUSTOM SEARCH")
	# define terms to filter for here, if not in request value is "N/A"
	terms = [
		"search",
		"arch_support",
		"terrain"
	]
	data = _generate_dictionary(request, terms)
	print (data)
	
	#data = "soft" #hardcode to test
	
	# FIX THIS FUNC, NOT WORKING
	return _search(FindQuery,data)


@irsystem.route('/', methods=['GET'])
def index():
	return render_template('index.html')
