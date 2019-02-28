Readme.txt
(1). Recommendations.html
	This is the HTML for the front-end page. Please open this page to view the Query, and the recommendations.
	The Implementation details and Originality contents are also mentioned in the same page.
(2). Solr
	In this assignment, I've used pysolr for indexing the text and querying the recommendations
	Using pip3, install the package for pysolr as follows:
	./pip3 install pysolr
	Installing Solr
		1. Download the package for Solr from the http://lucene.apache.org/solr/downloads.html
		2. Unzip the package downloaded
		3. Go to bin folder and run the command solr start
	Solr will be started at the below location:
	http://localhost:8983/solr
	Create a core in Solr UI with the name 'core0'. In my code, the requests are send to this core.
(3). NLTK
	For removing the stopwords and stemming, python nltk library is used.
	Using pip3, install the package for nltk	
	./pip3 install nltk
(4). Flask Server
	To handle the requests from the front end and also to send the query request to Solr, a python flask server is used. 
	For importing flask packages, use the pip3 command
	./pip3 install flask
	Flask is configured in the location: http://127.0.0.1:5000
(5). XLRD
	For handling excel file read and write, this project uses xlrd
	For importing this package, run the command
	./pip3 install xlrd
	
Content of Implementation Methods:
	"<h2>Content Collection</h2>" \
              "<p>The Data from Java Wikibooks was scrapped using Python BeautifulSoup</p>" \
              "<p> Data between two headers will be collected and stored together along with the corresponding code under this header</p>" \
              "<p>Once the data is scraped, all the special characters are removed both from code and the text</p>" \
              "<p>Then, the stop words are removed from the scrapped text using the stopwords library of python. This helped in providing more accurate results</p>" \
              "<p>Some of the URLs from Oracle tutorial were scraped. This provided better search results for some queries. <br>If we scrape the complete Oracle tutorial, the results will be predominantly from Oracle tutorial. So I proactively selected some specific URLs which could give us a balanced results</p>" \
              "<h2>Content Indexing</h2>" \
              "<p>Content Indexing is done using Pysolr</p>" \
              "<p>The Scraped data is stored in dictionary objects and the text of the scraped data and code are stored as seperate keys in the dictionary. This is helpful to search the code and text seperately. </p>" \
              "<p>The data is indexed to Solr using the command solr.add(). The complete dictionary object is indexed to Solr server. The keys of dictionary object are mainly, text, code and html/p>" \
              "<p>For the given data set, search is performed based on text and code, if both of them are available, and only on text if code is not available </p>" \
              "<h2>Web App</h2>" \
              "<p>To improve the human computer interaction, the web app is setup as a collapsible page</p>" \
              "<p>Based on the 10 queries, a query id is passed to the backend flask server, and the flask server removes the stopwords and special characters from the query and send it to Solr</p>" \
              "<p>The results are displayed under the collapsible header</p>" \
              "<p>The first 10 recommendations are displayed in the web page</p>"
			  
Content of Originality:
"<ul>" \
              "<li>Both the code and text are searched. The results with code and text gave better results than the ones from text only.</li>" \
              "<li>Some Contents from Oracle tutorial were scrapped. This helped to provide better recommendations for some queries, especially query 4</li>" \
              "<li>Better enhanced UI so everything could be find in one page without much scrolling</li>" \
              "<li>The indexing is done using Solr, which internally uses JSON Query DSL as the Domain Specific language and SOLR2703 for span queroes</li>" \
              "</ul>"