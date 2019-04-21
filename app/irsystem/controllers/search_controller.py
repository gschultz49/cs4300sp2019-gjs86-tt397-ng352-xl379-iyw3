from . import *  
# from app.irsystem.models.helpers import *	
# from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from app.irsystem.models.search import *

# helper, does searching
def _search (f, query):
	print (query)
	results = json.dumps(f(query))
	print (results)
	return results

# used for ajax retrieval
@irsystem.route('/custom_search')
def custom_search():
	query = request.args.get('search')
	return _search (FindSimilarShoes, query)

# used for ajax retrieval
@irsystem.route('/similar_search')
def similar_search():
	query = request.args.get('search')
	return _search(FindQuery, query)

@irsystem.route('/', methods=['GET'])
def index():
	return render_template('index.html')