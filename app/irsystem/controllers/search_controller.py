from . import *  
from app.irsystem.models.helpers import *

from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder


# from app.irsystem.models.search import *


# The actual IR system that will take the [query] and return the results as an array of objects
def ir_retrieve(query):
	print ("THE QUERY: {0}".format(query))

	# results =  FindSimilarShoes(query)
	# print ("RESULTS")
	# print (results)

	results = [
		{
			'similarShoes': ['Nike Air Zoom Pegasus 35'
				, 'Nike Flex Experience RN 7'
				, 'Asics Gel Kayano 25 OBI'
				, 'Nike Zoom Fly Flyknit'
				, 'New Balance FuelCore Sonic v2'
				, 'Nike LunarConverge'
			], 
		"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg",	'corescore': '94', 
			'similarity': 0.3093, 
			'shoeName': 'Adidas Solar Boost', 
			'relevantTerms': 
				['unit', 'becom', 'natur', 'athlet', 'spot', 't', 'race', 'didn', 'outsol', 'underfoot', 'peopl', 'laud']
		}
		, {'similarShoes': ['New Balance Vazee Breathe v2', 'On Cloudflyer', 'Nike Air Zoom Pegasus 35', 'New Balance Vazee Pace v2', 'Nike Air Zoom Structure 21', 'Under Armour Threadborne Slingflex'],"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg", 'corescore': '94', 'similarity': 0.2901, 'shoeName': 'Under Armour Speed Swift 2', 'relevantTerms': ['outsol', 'scheme', 'aesthet', 'emphas', 'unit', 'sturdi', 'ade', 'fa', 'prais', 'welcom', 'underfoot', 'like']}, {'similarShoes': ['Asics Gel Pulse 9', 'New Balance Fresh Foam Arishi', 'On Cloudflyer', 'Asics Gel Kayano 25 OBI', 'The North Face Flight RKT', 'Nike Air Zoom All Out Flyknit'],"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg", 'corescore': '94', 'similarity': 0.2756, 'shoeName': 'Under Armour Threadborne Slingflex', 'relevantTerms': ['scheme', 'underfoot', 'product', 'prais', 'aesthet', 'peopl', 'unit', 'effici', 'like', 'consid', 'experi', 'support']}, {'similarShoes': ['Inov-8 Mudclaw 300', 'Under Armour Threadborne Slingflex', 'Skechers GOrun Fast', 'Adidas Pure Boost Go', 'New Balance Fresh Foam Vongo v2', 'Under Armour SpeedForm Apollo 2'],"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg", 'corescore': '94', 'similarity': 0.2647, 'shoeName': 'Hoka One One Gaviota', 'relevantTerms': ['outsol', 'unit', 'trail', 'prais', 'regard', 'scheme', 'natur', 'underfoot', 'peopl', 'claim', 'effici', 'didn']}, {'similarShoes': ['Asics Gel Kayano 25 OBI', 'New Balance FuelCore Coast v4', 'Under Armour Charged Escape 2', 'Nike Air Zoom Pegasus 35', 'Asics Gel Pulse 9', 'Puma Hybrid Rocket Runner'],"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg", 'corescore': '94', 'similarity': 0.2611, 'shoeName': 'Nike Zoom Fly SP', 'relevantTerms': ['emphas', 'grippi', 'outsol', 'fa', 'ade', 'scheme', 'natur', 'underfoot', 'size', 'platform', 'mani', 't']}, {'similarShoes': ['Under Armour SpeedForm Apollo 2', 'Inov-8 Trailroc 270', 'Asics GT 1000 7 SP', 'Newton Motion 8', 'Hoka One One Cavu 2', 'Adidas Ultra Boost ST Parley'],"shoeImage": "https://cdn.runrepeat.com/i/nike/28162/nike-womens-air-zoom-pegasus-35-running-shoes-8-5-b-us-elemental-rose-barely-rose-vintage-wine-womens-elemental-rose-barely-rose-5627-main.jpg", 'corescore': '94', 'similarity': 0.2576, 'shoeName': 'Nike LunarGlide 9', 'relevantTerms': ['outsol', 'emphas', 'unit', 'trail', 'given', 'scheme', 'aesthet', 'like', 'peopl', 'protect', 'upper', 'effici']}]

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