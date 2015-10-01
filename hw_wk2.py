# Import csv to read in the file and import collections to
# get access to defaultdict()

import csv
import collections as col

# Part 1: Read in the data with csv.reader() and store it
#         in a list of lists called 'data'.
    
fname = r'f:\Python\DAT-DC-9\data\chipotle.tsv'

with open(fname,'rU') as f:
    data = [row for row in csv.reader(f,delimiter='\t')]

# Part 2: Separate the header and the data into two different lists.

column_names = data[0]
raw_data = data[1:]

# Part 3: Calculate the average price of an order.

# Create a list of prices, stripping out the beginning $ and 
# ending space characters.

price_list = [float(row[4].strip('$').strip()) for row in raw_data]

# Sum the prices across the new list.

price = 0
for i in range(0,len(price_list)):
    price = price + price_list[i]
    
# Create and print the average price for the 1834 orders in the data.
    
avg_price = round(price / 1834,2)

print(avg_price)
        
# Part 4: Create a list (or set) of all unique sodas and soft drinks 
#         that they sell.
        
# Make a list of the sodas, stripping the brackets.
        
soda_list = [row[3].strip('[').strip(']') for row in raw_data 
             if row[2] == "Canned Soda" or row[2] == "Canned Soft Drink"]

# Create the list of unique sodas. For practice, I did this 
# both as a set and a list.

unique_sodas = set(soda_list)     # Set version

unique_sodas2 = [var for pos, var in enumerate(soda_list) 
                 if soda_list.index(var) == pos]   # List version

print('\n',unique_sodas)
#print(unique_sodas2)

# Part 5: Calculate the average number of toppings per burrito.

# First calculate the number of burritos, ignoring the quantity column.

num_burritos = 0
for row in raw_data:
    if "Burrito" in row[2]:
        num_burritos += 1
        
# burrito_toppings is a list which represents the number of 
# toppings in each burrito.

burrito_toppings = [len(row[3].split(',')) for row in raw_data 
                    if "Burrito" in row[2]]
                        
# Calculate the average number of toppings per burrito and pring
# the results.
                        
avg_num_toppings = float(sum(burrito_toppings) / num_burritos)

print('\n',round(avg_num_toppings,2))

# Part 6: Create a dictionary in which the keys represent chip orders and
# the values represent the total number of orders.

# Note that I use the .replace('-',' ') because it seems clear that
# the hyphen is causing the same item to be split into two groups.
# So I remove it to combine them. Note, though, that I am not 
# worrying that "Coke" and "Coca Cola" are technically the same thing.

chips = [[row[2].replace('-',' '),int(row[1])] for row in raw_data 
          if "Chips" in row[2]]
              
# Use defaultdict() from the collections package to both initialize
# a new dict and sum the quantities of the chips across the different
# types, outputing the unique pairs to the dictionary created by 
# defaultdict().

chips_dict = col.defaultdict(int)
for k, v in chips:
    chips_dict[k] += v
    
print('\n', chips_dict)

# Bonus: Think of a question about this data that interest you,
#        and answer it!

# One thing I had wondered was whether the differences in the prices
# of a chicken burrito were because of a price change or the orders
# being taken in a separate location. The data seem to indicate a 
# different location because of how soda is treated. We can observe
# this by looking at orders with both a burrito and soda purchase.

# First grab the rows which contain either Burrito or Canned.

ch_bur = [[int(row[0]),[row[2],float(row[4].strip('$').strip())]] 
          for row in raw_data
          if "Burrito" in row[2] or "Canned" in row[2]]
              
# Call defaultdict() to initialize our new dictionary and to map
# each order (all the orders will take one value) to the order_id
# which will be the key.

loc_dict = col.defaultdict(list)

for k, v in ch_bur:
    loc_dict[k].append(v)

# The next step creates a new dictionary from the
# old one which stored only the (key,value) pairs which contained
# both a Burrito order and a Canned drink order. This is done by 
# going into the list of values and creating indicator variables
# for when each [item, price] pair contains the word "Burrito"
# or "Canned." Then, if both indicators are 1 (so both "Burrito" 
# and "Canned are in the value) at some point in the value, then 
# assign the original (key, value) to the new dictionary

refined_dict = {}

for k in loc_dict:
    temp_list = []
    burrito = 0
    canned = 0
    v = loc_dict[k]
    for pair in v:
        if "Burrito" in pair[0]:
            temp_list.append(pair)
            burrito = 1
        if "Canned" in pair[0]:
            temp_list.append(pair)
            canned = 1
    if burrito == 1 and canned == 1: 
        refined_dict[k] = temp_list
    
print('\n',refined_dict)

# This shows that if the order calls the drink a "Canned Soda," the 
# prices as a whole are cheaper (probably a different tax rate or
# something) versus calling the drink a "Canned Soft Drink." Having
# the two names with the two prices indicates that it is more likely
# that the orders take place in different locations.

