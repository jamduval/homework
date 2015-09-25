## Homework Assignment - Week 1

1. _Using_ chipotle.tsv _in the_ data _subdirectory:_
  * __Look at the head and the tail, and think for a minute about how the data is structured. 
What do you think each column means? What do you think each row means? Tell me!__       
    * _order_id_ is a specific customer order identifier, so one customer can order multiple items.
_quantity_ represents how many of each _item name_ was ordered. _item_name_ is the specific
item that was ordered from the menu. _choice_description_ is a list of lists that represents each of the optional 
choices that the customer chose in reference to their selected _item_name_; and this list is set up
as [[list of salsas],[list of other toppings]]. _item_price_ is 
the cost of the _quantity_ and _item_name_ combo. Each row represents an item ordered by a customer, where 
customers can order multiple items.    
  * __How many orders do there appear to be?__
    * There appear to be 1834 orders.
  * __How many lines are in the file?__
    * There are 4624 lines in the file; 4623 lines of data and 1 blank line which may represent either the "search tab"
  * __Which burrito is more popular, steak or chicken?__
    * __Chicken__ is more popular.
  * __Do chicken burritos more often have black beans or pinto beans?__
    * Chicken burritos more often have __black beans__.

2. _Count the number of occurrences of the word 'dictionary' (regardless of case) across all files in the DAT9 repo._
  * After first using 'git clone https://github.com/vybstat/dat9.git', I then entered the following into Git:
'grep -ri "Dictionary" .'; which produced the following __two__ occurrences of the word 'dictionary' in the DAT9 repo:
"./README.md:2. Count the number of occurrences of the word 'dictionary' (regardless of case) across all files in the DAT9 repo.
./project/README.md:* **Data dictionary (aka "code book"):** description of each variable, including units."

3. _Optional: Use the command line to discover something "interesting" about the Chipotle data. The advanced
commands may be helpful to you._
  * In my opinion, something "interesting" to me would be if you cut the data and store it into a new file by
doing; 'cut -f3,5 chipotle.tsv > prices.tsv' and then performing a sort by; 'sort prices.tsv'. Excluding the 
differences in price caused by the addition of guacamole, some _item_price_ values are different than others. 
For example, the chicken bowl has 3 item prices of $8.49, $8.50, and $8.75. Why? If these customer orders are not
in order of when they took place, this could be caused by a price hike in the value of their bowls. They may also
not have been placed at the same chipotle, so these orders could be in different counties or states where the tax on food
is different which might cause a difference in the price. If this were a relational database, there might be an 
additional table to help us find out.
