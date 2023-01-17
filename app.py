import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from flask import Flask, jsonify
from flask import request
import time
app = Flask(__name__)

@app.route('/')  
def hello():
    url = request.args.get('url')
    if url:
        url = unquote(url)    
    print(url)
    response = requests.get(str(url))
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        if a.get_text().startswith('http'):
            print(a['href'])
            return a['href']
    return "N/A"
    
@app.route('/performance')
def check_performance():
    website = request.args.get('url')    
    start_time = time.time()
    response = requests.get(str(website))
    end_time = time.time()
    total_time = end_time - start_time
    return jsonify({"website": website, "response_time": total_time})

if __name__ == '__main__':
    app.run(debug=True)
