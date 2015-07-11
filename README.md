#Howdy
Thanks for taking the time to look at this program!

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
run program like so:
```
python3 simpleweb.py
```

Then point your browser to the host running the web interface to http://hostname:5959/

example urls (with nordstrom plugin):

category:
* http://shop.nordstrom.com/c/mens-polo-shirts?dept=8000001&origin=topnav
* http://shop.nordstrom.com/c/diaper-bag?dept=8000001&origin=topnav

product:
* http://shop.nordstrom.com/s/charles-by-charles-david-pact-pump/4111984?origin=category
* http://shop.nordstrom.com/s/cupcakes-and-cashmere-santa-ana-pleated-skirt/4097152?origin=category

example urls (with best guess global plugin / only does category pages for now):
* https://www.jcrew.com/girls_category/dresses.jsp

#TODO
* General error handling
* The GLOBAL plugin could do FAR more
  *  Plugin could run as a seperte process/many processes and listen to requests on a mq and service them async. This would speed up things what with all the spinning up time a headless webkit browser takes.
  *  Currently all it does is load the url requested to be fetched and then Waits for page to render
   *  Iterates though all links that contain an img (via xpath)
     *  Saves some info about these elements (element id, left,top,width,height, ceneter of element x/y and pixel/area count and it's url)
     *  If that a area is greater than 3% of the screen it then considers it an important link/img and adds it to a list
   *  Iterates though all text elements that contain a $
     * grabs similar info and this time checks to make sure the element size is less than 3%
   *  Iterates through all links that contian an image and finds the closest (pixel distance) element center that contain what appeared to be a dollar amount.
   *  Returns all that info
  *  This plugin could be far improved in any number of ways
    *  I would say it "happens" to work in sites like jcrew because jcrew has a tags with a child img tag. The xpath could be cleaned up to include all a tags with an img descendent but I but this could get wonky.
    *  To catch the difference between a category page and a product page it could see if there are a "grid" of img/a tags that share similar or exact left and tops. If an element shares it's left and top tag with other >x% screen size elements we can start to infer we're looking at a grid of data.
    *  We could do some LCA or other tree traversal techniques to find all there "grid" items and maybe start to infer/guess some structure on unknown pages. Might could find the "product listing" section with this technique. Once we have the section we could look for the most repeated class or tag that is closest to the root of that product listing setion. We could probably assume those are the product wrappers. We could then look for dollar amounts inside those product wrappers rather than just general pixel distance.
    *  We could also do some guessing based on color and size of various elements that contain price. A bigger element that contains a price might indicate the actual or sale price. Could also look for color contrast, red on white being more likely to be the price than black on white. Ignore Strikethroughs, etc.
    *  Could do ocr to see if the text the html shows would be readable to the customer out there. If not it's probably not indicative of imporant information.
    *  Many, many other things.
#Issues
* Doesn't have robust error handling for all the various timeouts or page rendeirng issues that could occur. It feels like that is out of scope for this assignment other than the assignment should generally work.
* Nordstrom plugin doesn't detect info on psuedo-category pages like:
  * http://shop.nordstrom.com/c/sale
  * Theses pages contain post-document ready js injections which feel out of scope for this assignment.
* Global plugin is very simple, won't detect many pages as being category pages and those it does detect will only return VERY limited info like url to product and a best guess as to theprice of that product.
 

#General Program Flow
* User enters a url on the main page and clicks fetch
* js sends off a api/json request to an api endpoint containing the action to perform (fetch) and the url to perform it on (the url entered)
* the web interface then goes into a waiting mode polling the same endping looking for results from that url
  *  There is no error handling here, no on failure, no on error, no timeouts. Those feel out of scope for this proof of concept
  *  This polling api endpoint aquires a thread lock on essentially a global "results" variable to see if we have results for that item.
*  The server process interprets this api request and adds it to a thread safe queue
*  a worker thread in the server polls the queue and once it has an item it attempts to handle it
  *  the worker process will example the url it see and parse it up.
  *  if there is a registered plugin for handling the hostname of the url it is assigned it will pass it off to that registered handler/function
  *  if there is NOT a registered plugin for handling the hostname of the url it is assigned it will pass it off to a very simple GLOBAL handler
*  Once the handler function returns results, the worker thread acquires a lock on the global results var and posts the results there
*  The worker thread also occasionally purges old results from the results var so they arn't stale
*  Once results show up the api endpoint the web interface presents a pre-tagged json of the structured data it found
