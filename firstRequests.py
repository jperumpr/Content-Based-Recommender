import requests
from bs4 import BeautifulSoup,NavigableString,Tag
import csv
import pysolr
import json
import re
import xlrd
from flask import Flask, session, redirect, url_for, escape, request
from lxml import html
from flask_cors import CORS

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



app = Flask(__name__)
app.secret_key = "any"
cors = CORS(app, resources={"*"}, allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Origin"],
            supports_credentials=True)

def scrapy():
    URL = "https://en.wikibooks.org/wiki/Java_Programming"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    stop_words = set(stopwords.words('english'))

    quotes = []  # a list to store quotes
    scrapList = []
    table = soup.find('div', attrs={'id': 'mw-content-text'})
    for a in table.find_all('a', href=True):
        if("/wiki/Java_Programming" in a['href']):
            quotes.append(a['href'])
    quotes = quotes[10:]
    count =0
    i=0

    for val in quotes:
        url = "https://en.wikibooks.org" + val
        scrapDict = {}
        #print(val)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', attrs={'id': 'mw-content-text'})
        h1 = ["h2","h3"]
        for header in table.find_all(h1):

            print(count)
            nextNode = header
            count += 1
            fname = "f" + str(count) + ".txt"
            f = open(fname, "w+", encoding='utf-8')
            text =" "
            curnode = ""
            codehtml = ""
            codetext = ""
            scrapDict["title"] = nextNode.get_text(strip=True).strip()

            print("title = ",scrapDict["title"])
            while True:
                nextNode = nextNode.nextSibling
                if nextNode is None:
                    break

                if isinstance(nextNode, Tag):
                    if nextNode.name in {"h2","h1","h3"}:
                        break
                    #print(nextNode)
                    #f.write(str(nextNode))
                    curnode += str(nextNode)
                    if nextNode.name == "table":
                        codehtml = str(nextNode)
                        codenotag1 = re.sub("<.*?>", " ", codehtml)
                        codenotag = re.sub("\n", "", codenotag1)
                        codetext += codenotag
                        #print(codehtml)
                    else:
                        curtag = str(nextNode)
                        notag = re.sub("<.*?>", " ", curtag)
                        #output = nextNode.get_text(strip=True).strip()
                        text += notag
                        #f.write(output)

            word_tokens = word_tokenize(text)
            filtered_text = [w for w in word_tokens if not w in stop_words]

            filtered_sentence = ""
            for w in filtered_text:
                filtered_sentence += " "
                filtered_sentence += w

            scrapDict["html"] = curnode
            scrapDict["text"] = filtered_sentence
            #scrapDict["codehtml"] = codehtml
            scrapDict["codetext"] = codetext
            jsonData = json.dumps(scrapDict)
            f.write(jsonData)
            scrapList.append(scrapDict)
            f.close()
            f1 = open(fname,"r",encoding='utf-8')
            readFile = f1.read()
            jsonRead = json.loads(readFile)
            #print(jsonRead["text"])
            f1.close()


def scrapyOracle():
    URL = "https://docs.oracle.com/javase/tutorial/reallybigindex.html"
    r = requests.get(URL)
    quotes = html.fromstring(r.content).xpath('//a/@href')
    #soup = BeautifulSoup(r.content, 'html5lib')


    print(quotes)
    stop_words = set(stopwords.words('english'))

    quotes = quotes[10:]

    quotes = ["https://docs.oracle.com/javase/tutorial/java/IandI/polymorphism.html", "https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html","https://docs.oracle.com/javase/tutorial/java/IandI/objectclass.html","https://docs.oracle.com/javase/tutorial/java/IandI/multipleinheritance.html","https://docs.oracle.com/javase/tutorial/java/IandI/override.html","https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html"]
    scrapList = []
    #table = soup.find('div', attrs={'id': 'a href'})
    count = 486
    for url in quotes:
        #url = "https://docs.oracle.com/javase/tutorial/" + val
        scrapDict = {}
        # print(val)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', attrs={'id': 'PageContent'})
        h1 = ["h2", "h3"]
        taglists = table.children
        print(taglists)
        tags = list(taglists)
        flag = 0
        for val in tags:
            if val in h1:
                flag=1


        for header in table.find_all(h1):
            flag =1
            print(count)
            nextNode = header
            count += 1
            fname = "f" + str(count) + ".txt"
            f = open(fname, "w+", encoding='utf-8')
            text = " "
            curnode = ""
            codehtml = ""
            codetext = ""
            scrapDict["title"] = nextNode.get_text(strip=True).strip()

            print("title = ", scrapDict["title"])
            while True:
                nextNode = nextNode.nextSibling
                if nextNode is None:
                    break

                if isinstance(nextNode, Tag):
                    if nextNode.name in {"h2", "h1", "h3"}:
                        break
                    # print(nextNode)
                    # f.write(str(nextNode))
                    curnode += str(nextNode)
                    if nextNode.name == "table":
                        codehtml = str(nextNode)
                        codenotag1 = re.sub("<.*?>", " ", codehtml)
                        codenotag = re.sub("\n", "", codenotag1)
                        codetext += codenotag
                        # print(codehtml)
                    else:
                        curtag = str(nextNode)
                        notag = re.sub("<.*?>", " ", curtag)
                        # output = nextNode.get_text(strip=True).strip()
                        text += notag
                        # f.write(output)

            word_tokens = word_tokenize(text)
            filtered_text = [w for w in word_tokens if not w in stop_words]

            filtered_sentence = ""
            for w in filtered_text:
                filtered_sentence += " "
                filtered_sentence += w

            scrapDict["html"] = curnode
            scrapDict["text"] = filtered_sentence
            # scrapDict["codehtml"] = codehtml
            scrapDict["codetext"] = codetext
            jsonData = json.dumps(scrapDict)
            f.write(jsonData)
            scrapList.append(scrapDict)
            f.close()
            f1 = open(fname, "r", encoding='utf-8')
            readFile = f1.read()
            jsonRead = json.loads(readFile)
            # print(jsonRead["text"])
            f1.close()

        if flag ==0:
            text = " "
            curnode = ""
            codehtml = ""
            codetext = ""
            curnode = str(table)
            nextNode = str(table)
            print(nextNode)
            curtag = str(nextNode)
            fname = "f" + str(count) + ".txt"
            f = open(fname, "w+", encoding='utf-8')
            notag = re.sub("<.*?>", " ", curtag)
            # output = nextNode.get_text(strip=True).strip()
            text += notag
            word_tokens = word_tokenize(text)
            filtered_text = [w for w in word_tokens if not w in stop_words]

            filtered_sentence = ""
            for w in filtered_text:
                filtered_sentence += " "
                filtered_sentence += w

            scrapDict["html"] = curnode
            scrapDict["text"] = filtered_sentence
            # scrapDict["codehtml"] = codehtml
            scrapDict["codetext"] = codetext
            jsonData = json.dumps(scrapDict)
            f.write(jsonData)
            scrapList.append(scrapDict)
            f.close()



def solrAddIndex():
    solr = pysolr.Solr('http://localhost:8983/solr/core0')
    dictList = []
    for i in range(1,497):
        fname = "f"+ str(i) + ".txt"
        f1 = open(fname, "r", encoding='utf-8')
        readFile = f1.read()
        jsonRead = json.loads(readFile)
        #print(jsonRead["text"])

        dict ={}

        dictText = {"text" : jsonRead["text"]}
        dicTextHtml = {"texthtml" :  jsonRead["html"] }
        codeText = {"codetext" : jsonRead["codetext"]}
        #codeHtml = {"codehtml" : jsonRead["codehtml"]}
        #print("jsonRead[html] " ,jsonRead["html"])
        dict["id"] = i
        dict["title"] = fname
        dict["doc1"] = jsonRead["text"]
        dict["code"] = jsonRead["codetext"]
        dict["dochtml1"] = jsonRead["html"]
        #dict["codehtml"] = jsonRead["codehtml"]
        #solr.add(dict)
        dictList.append(dict)

        f1.close()
    print(dictList[1])
    solr.add(dictList)
    solr.commit()


@app.route("/search", methods = ['POST'])
def search():
    #cors = CORS(app, resources={"*"}, allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)
    print("searching")

    #excelpath = "C:\Users\jithin.perumpraljohn\PycharmProjects\scrapy\data.xlsx"
    sheet = xlrd.open_workbook(r"data.xlsx")

    first_sheet = sheet.sheet_by_index(0)
    print("reading row")
    # read a row
    print(first_sheet.row_values(1,1))

    stop_words = set(stopwords.words('english'))

    srcdictlist = []
    for i in range(1,11):
        sourcedict = {}
        sourcedict["key"] = i

        raw_source = first_sheet.row_values(i,1)
        word_tokens = word_tokenize(str(raw_source))
        filtered_text = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = ""
        for w in filtered_text:
            filtered_sentence += " "
            filtered_sentence += w
        #print("filtered sentence= ",filtered_sentence)

        sourcedict["text"] = filtered_sentence
        if first_sheet.row_values(i,2) != None:
            code1 = first_sheet.row_values(i,2)
            code2 = code1[0]
            code = re.sub('[^A-Za-z0-9]+', ' ', code2)
            if len(code)!=0:
                sourcedict["code"] = code
                print( sourcedict["code"])
        srcdictlist.append(sourcedict)

    #print(srcdictlist)

    solr = pysolr.Solr('http://localhost:8983/solr/core0')
    req = request.get_json()
    #print(req)
    qnum = req["id"]
    qno = int(qnum)
    if qno ==0:
        #print("qno==0")
        res = "<h2>Content Collection</h2>" \
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


        return res
    if qno == 11:
        res = "<ul>" \
              "<li>Both the code and text are searched. The results with code and text gave better results than the ones from text only.</li>" \
              "<li>Some Contents from Oracle tutorial were scrapped. This helped to provide better recommendations for some queries, especially query 4</li>" \
              "<li>Better enhanced UI so everything could be find in one page without much scrolling</li>" \
              "<li>The indexing is done using Solr, which internally uses JSON Query DSL as the Domain Specific language and SOLR2703 for span queroes</li>" \
              "</ul>"
        return res
    print("qno=",qno)
    query1 = srcdictlist[qno-1]["text"]
    query = str(query1)
    qlen = len(query)
    query = query[2:-15]

    query2 = re.sub(":", "", query)
    query = re.sub('[^A-Za-z0-9]+', ' ', query2)
    print(query)
    #print("query=", query2)
    if "code" in srcdictlist[qno-1]:
        codequery = srcdictlist[qno-1]["code"]
        print("codequery = ", codequery)
        results = solr.search("doc1: "+ query +", code: " + codequery)
    else:
        results = solr.search("doc1: " + query)
    ret = ""
    i = 0

    for val in results:
        if i== 10:
            break
        i+=1
        solr_res = val['dochtml1'][0]
        #print(solr_res.replace('\n', ''))
        ret += "<h1>Recommendation " + str(i) + "</h1>"
        ret += solr_res + " "
        if 'codehtml' in val:
            ret += str(val['codehtml']) + " "

    #print(ret)
    return ret

if __name__ == "__main__":
    scrapy()
    scrapyOracle()
    solrAddIndex()
    app.run()

