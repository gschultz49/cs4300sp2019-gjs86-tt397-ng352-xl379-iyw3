import pandas as pd 
from skimage import io
import pickle

reviews = pd.read_csv('4_15_2019.tsv', sep='\t')
df_reviews = reviews[['shoeName','shoe_image']]
dictionary = {}
for i in range(10):
	shoe_name = df_reviews.iloc[i]["shoeName"]
	shoe_image = df_reviews.iloc[i]["shoe_image"]
	shoe_image_array = io.imread(shoe_image)[:, :, :-1]
	dictionary[shoe_name] = shoe_image_array
print(len(dictionary))
pickle.dump( dictionary, open( "shoes_images.p", "wb" ) )

