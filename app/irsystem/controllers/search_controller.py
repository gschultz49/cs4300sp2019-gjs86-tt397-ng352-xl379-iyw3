from . import *  
from app.irsystem.models.search import *
from flask import jsonify

# helper
def autosuggester(q, f):
	return jsonify(f(q))

# helper, does searching
def _search (f, query):
	print (query)
	results = json.dumps(f(query['search'],query))
	# print (results)
	return results


def _searchs (f, query):
	print (query)
	results = json.dumps(f(query))
	# print (results)
	return results

def _generate_dictionary(request, termsDict):
	ISARRAY = ["terrain", "arch_support", "price"]
	for t in termsDict:
		if t in request.args or t in ISARRAY:
			if type(termsDict[t]) == list:
				termsDict[t] = request.args.getlist(t+"[]")
			else:
				termsDict[t] = request.args.get(t)
		else:
			termsDict[t] ="N/A"
	# print (termsDict)
	return termsDict


# Grabs multiple similar shoes
@irsystem.route('/similar_search')
def similar_search():
	print ("IN SIMILAR SEARCH")
	return _searchs (FindSimilarShoes, request.args.get("search"))

# Grabs a single shoe for similar search
@irsystem.route('/similar_search_individual')
def similar_search_individual():
	return _searchs(FindShoe, request.args.get("search"))



# Similar shoe autosuggester
@irsystem.route('/similar_shoe_autosuggest')
def similar_shoe_autosuggest():
	print("SIMILAR SHOE AUTOSUGGEST")
	return autosuggester(request.args.get("q"), CompleteName)

# Custom shoe autosuggester
@irsystem.route('/custom_shoe_autosuggest')
def custom_shoe_autosuggest():
	print("CUSTOM SHOE AUTOSUGGEST")
	# change this function !
	return autosuggester(request.args.get("q"), CompleteWord)

# used for ajax retrieval
@irsystem.route('/custom_search')
def custom_search():
	print ("IN CUSTOM SEARCH")
	# define terms to filter for here, if not in request value is "N/A"
	terms = {
		"search": None,
		"terrain":[],
		"arch_support": [],
		# "gender": None,
		# "weight": None,
		# "price": 1000
		"price": []
	}

	data = _generate_dictionary(request, terms)
	return _search(FindQuery,data)


@irsystem.route('/', methods=['GET'])
def index():
	return render_template('index.html')
