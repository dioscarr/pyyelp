
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from flask import Flask
from flask import request
app = Flask(__name__)
@app.route('/')  
def hello():
    url = request.args.get('url')
    if url:
        url = unquote(url)    
    
    print(url)
    # url = 'https://www.yelp.com/biz/the-swanson-perry?adjust_creative=ZtipivwuIGdHJE7C3EO4pg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=ZtipivwuIGdHJE7C3EO4pg'
    response = requests.get(str(url))
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        if a.get_text().startswith('http'):
            print(a['href'])
            return a['href']
    return "N/A"
if __name__ == '__main__':
    app.run(debug=True)
