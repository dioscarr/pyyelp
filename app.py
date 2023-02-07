import requests
from urllib.parse import urlparse
from validate_email import validate_email
from bs4 import BeautifulSoup
from urllib.parse import unquote
from flask import Flask, jsonify
from flask import request
import re
import time
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')  
def hello():
    url = request.args.get('url')
    if url:
        url = unquote(url)
    try:
        response = requests.get(str(url))
        soup = BeautifulSoup(response.text, 'html.parser')

        for span in soup.find_all('span',attrs={"class":"icon--24-external-link-v2" }):
            parent = span.find_parent('a', href=True)
            if parent:           
                return parent['href']
    except Exception as e:
        return "Exception"
    return "Exception"
    
    
@app.route('/performance' , methods=['GET'])
def check_performance():
    website = request.args.get('url')    
    start_time = time.time()
    response = requests.get(str(website))
    end_time = time.time()
    total_time = end_time - start_time
    return jsonify({"website": website, "response_time": total_time})

@app.route('/findemail', methods=['GET'])
def create_map():
    retry_count = 0
    start_url = request.args.get('url')
    visited_urls = set()
    queue = [start_url]
    email_addresses = set()
    session = requests.Session()
    parsed_start_url = urlparse(start_url)
    while queue:
        retry_count = retry_count + 1
        url = queue.pop(0)
        visited_urls.add(url)
        try:
            response = session.get(str(url))
            content_type = response.headers.get('content-type')
            if content_type:
                if 'charset=' in content_type:
                    encoding = content_type.split('charset=')[-1]
                    response.encoding = encoding
            email_regex = r'mailto:(\S+)'
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):               
                match = re.search(email_regex, link['href'])
                href = link.get('href')
                if match and len(link.get('href').split(':')[1]) < 90:
                    try:
                        if link.get('href').startswith('mailto:'):        
                            email_addresses.add(link.get('href').split(':')[1])                                             
                            return jsonify({"url":start_url,"emails":list(email_addresses)})
                    except ValueError as e:
                        email_addresses.add("N/A")
                        return jsonify({"url":start_url,"emails":list(email_addresses)}) 
        except Exception as e:
            email_addresses.add("N/A")
            return jsonify({"url":start_url,"emails":list(email_addresses)})  
        
        if retry_count is 3:
            email_addresses.add("N/A")
            return jsonify({"url":start_url,"emails":list(email_addresses)})  
        else: 
            retry_count = retry_count + 1           
            
    email_addresses.add("N/A")        
    return jsonify({"url":start_url,"emails":list(email_addresses)})    
if __name__ == '__main__':
    app.run(debug=True)