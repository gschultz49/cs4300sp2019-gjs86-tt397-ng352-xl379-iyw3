from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "TEAM SOLEMATE"
net_id = "dnm"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	netIDS = [
		"gjs86",
		"tt397",
		"ng352",
		"xl379",
		"iyw3"
	]
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, netIDS = netIDS)


@irsystem.route('/splash', methods=['GET'])
def splash():
	return render_template('splash.html')



