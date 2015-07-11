#Howdy
Thanks for taking the time to look at this program!

#Issues
* Doesn't have robust error handling for all the various timeouts or page rendeirng issues that could occur. It feels like that is out of scope for this assignment other than the assignment should generally work.
* Nordstrom plugin doesn't detect info on psuedo-category pages like:
  * http://shop.nordstrom.com/c/sale
  * Theses pages contain post-document ready js injections which feel out of scope for this assignment.
* Global plugin is very simple, won't detect many pages as being category pages and those it does detect will only return VERY limited info like url to product and a best guess as to theprice of that product.

#Dependencies
This depends on python 3+ and needs the following pip3 modules:
* flask
* requests
* beautifulsoup4
* selenium (optional but it will improve extraction where there is no predefined plugin)

non-python packages:
* phantomjs 
  * (optional but it will improve extraction where there is no predefined plugin) it can be found in some linux dist repos or compiled from source here: http://phantomjs.org/download.html


#Example Usage:
example urls (with nordstrom plugin):

category:
http://shop.nordstrom.com/c/mens-polo-shirts?dept=8000001&origin=topnav
http://shop.nordstrom.com/c/diaper-bag?dept=8000001&origin=topnav

product:
http://shop.nordstrom.com/s/charles-by-charles-david-pact-pump/4111984?origin=category
http://shop.nordstrom.com/s/cupcakes-and-cashmere-santa-ana-pleated-skirt/4097152?origin=category

example urls (with best guess global plugin / only does category pages for now):
https://www.jcrew.com/girls_category/dresses.jsp
