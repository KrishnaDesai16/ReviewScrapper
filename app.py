from flask import Flask ,render_template,request
from bs4 import BeautifulSoup as sb
import requests
from urllib.request import urlopen as uReq
from flask_cors import CORS,cross_origin

app=Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
@cross_origin()
def Homepage():
        return render_template('index.html')


@app.route('/scrap',methods=['POST'])
def index():
    if request.method == 'POST':

        SearchString = request.form['content'].replace(" ", "")
        try:

                flipkart_url = 'https://www.flipkart.com/search?q=' + SearchString
                uClient = uReq(flipkart_url)
                flipkartpage = uClient.read()
                uClient.close()
                flipkart_html = sb(flipkartpage, 'html.parser')
                bigboxes = flipkart_html.find_all('div', 'bhgxx2 col-12-12')
                del bigboxes[0:3]  # the first 3 members of the list do not contain relevant information, hence deleting them.
                box = bigboxes[0]  # taking the first iteration (for demo)
                productLink = "https://www.flipkart.com" + box.div.div.div.a['href']  # extracting the actual product link
                prodRes = requests.get(productLink)  # getting the product page from server
                prod_html = sb(prodRes.text, "html.parser")  # parsing the product page as HTML
                commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})  # finding the HTML section containing the customer comments


                reviews = []
                for commentbox in commentboxes:
                    try:
                        name = commentbox.div.div.find_all('p', {'class', '3LYOAd _3sxSiS'})[0].text
                    except:
                        name = 'No Name'
                    try:
                        rating = commentbox.div.div.div.div.text
                    except:
                        rating = 'No rating'
                    try:
                        commentHead = commentbox.div.div.div.p.text
                    except:
                        commentHead = 'No  commentheading'
                    try:
                        comtag = commentbox.div.div.find_all('div', {'class', ''})
                        custcommt = comtag[0].div.text


                    except:
                        custcommt = 'No Customer Comment'
                    mydict = {"Product": SearchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                              "Comment": custcommt}
                    reviews.append(mydict)

                return render_template("result.html", reviews=reviews)
        except:
            return "Somthing Wrong"




if __name__ == '__main__':
    app.run(port=8000, debug=True)