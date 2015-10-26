'''
OPTIONAL WEB SCRAPING HOMEWORK

First, define a function that accepts an IMDb ID and returns a dictionary of
movie information: title, star_rating, description, content_rating, duration.
The function should gather this information by scraping the IMDb website, not
by calling the OMDb API. (This is really just a wrapper of the web scraping
code we wrote above.)

For example, get_movie_info('tt0111161') should return:

{'content_rating': 'R',
 'description': u'Two imprisoned men bond over a number of years...',
 'duration': 142,
 'star_rating': 9.3,
 'title': u'The Shawshank Redemption'}

Then, open the file imdb_ids.txt using Python, and write a for loop that builds
a list in which each element is a dictionary of movie information.

Finally, convert that list into a DataFrame.
'''

# Import the functions

import requests
import pandas as pd
from bs4 import BeautifulSoup

# define a function that accepts an IMDb ID and returns a dictionary of movie information
def get_movie_info(imdb_id):
    r = requests.get('http://www.imdb.com/title/' + imdb_id + '/')
    b = BeautifulSoup(r.text)
    info = {}
    info['title'] = b.find(name='span', attrs={'class':'itemprop', 'itemprop':'name'}).text
    info['star_rating'] = float(b.find(name='span', attrs={'itemprop':'ratingValue'}).text)
    info['description'] = b.find(name='p', attrs={'itemprop':'description'}).text.strip()
    info['content_rating'] = b.find(name='meta', attrs={'itemprop':'contentRating'})['content']
    info['duration'] = int(b.find(name='time', attrs={'itemprop':'duration'}).text.strip()[:-4])
    return info

# test the function
get_movie_info('tt2234222')

# open the file of IDs (one ID per row), and store the IDs in a list
fname = r'f:/git_repositories/DAT-DC-9/data/imdb_ids.txt'

id_list=[]   # initialize the list
with open(fname) as f:
    for row in f:
        id_list.append(row.strip()) #String the new lines.

# get the information for each movie, and store the results in a list
movie_dict_list=[]
for row in id_list:
    movie_item = get_movie_info(row)
    movie_dict_list.append(movie_item)

print(movie_dict_list)  #Print to test that the function worked.

# check that the list of IDs and list of movies are the same length
print(len(id_list))
print(len(movie_dict_list))

# convert the list of movies into a DataFrame

# Create a temporary dataframe for the info
temp_dict1 = pd.DataFrame(movie_dict_list)

# Create a temporary dataframe for the ids
temp_dict2 = pd.DataFrame(id_list)
temp_dict2.rename(columns={0:'imdb_id'}, inplace=True)

# Merge the two together (and since they were lists, order was preserved)
imdb_df = pd.concat([temp_dict1,temp_dict2],axis=1)

'''
Another IMDb example: Getting the genres
'''

# read the Shawshank Redemption page again

r = requests.get('http://www.imdb.com/title/tt0111161/')
b = BeautifulSoup(r.text)
print(b)

# only gets the first genre

b.find(name='div', attrs={'class':'infobar'}).find(name='a').find(name='span').text

# gets all of the genres

genre_prep = b.find(name='div', attrs={'class':'infobar'}).find_all(name='span',attrs={'itemprop':'genre'},text=True)

# stores the genres in a list

genres=[]
for row in genre_prep:
    var_g = row.text #grab just the text from the html in the genre_prep list.
    genres.append(var_g)
    
print(genres)  #Output the list

'''
Another IMDb example: Getting the writers
'''

# attempt to get the list of writers (too many results)

names = b.find(name='div').find_all(name='span',attrs={'class':'itemprop','itemprop':'name'})

# limit search to a smaller section to only get the writers

#Do the same type of loop as before to output the writers to a list.

writers = []
for row in names[2:4]:
    var_w = row.text
    writers.append(var_w)
    
print(writers) #output the writers

'''
Another IMDb example: Getting the URLs of cast images
'''

# find the images by size

# I do not understand the "by size" part to this question. They are all 44 by 32.

photo_list = b.find(name='table',attrs={'class':'cast_list'}).find_all(name='td',attrs={'class':'primary_photo'})

# check that the number of results matches the number of cast images on the page

len(photo_list) # This equals 15 which equals the number of cast images on the page.
                # Also, the last href line for the photo_list ends in i15 which likely means image 15.

# iterate over the results to get all URLs

# I originally used the "src" reference for the photo but double checking in a browser
# yielded no actual photo, so I changed the reference to "loadlate" which does.

photo_urls = []
for row in photo_list:
    temp_var = row.find(name='img')['loadlate']
    photo_urls.append(temp_var)
    
print(photo_urls) 
