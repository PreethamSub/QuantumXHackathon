from flask import Flask,request,jsonify, make_response, abort
from flask_cors import CORS, cross_origin
import requests
from transformers import pipeline
import wikipedia
from keybert import KeyBERT
import base64
import json
import random

# Set your WordPress site URL and authentication token
wordpress_url = '<WordPress_url>'
upload_url = wordpress_url + '?rest_route=/wp/v2/media/'

# The wordpress username and application password
username = '<Your_Username>'
password = '<Your_application_password>'

credentials = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
headers = {
    'Authorization': f'Basic {credentials}'
}

print('Loading Model')
summarizer = pipeline("summarization", r"\QH\summarizer")
kw_model = KeyBERT()
print('Loaded Model')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def download_image(url, file):
    with open(file, 'wb') as f:
        f.write(requests.get(url).content)

@app.route('/generate' , methods=["POST"])
def index():
    data = request.get_json()
    print(data)
    keywords = kw_model.extract_keywords(data['prompt'], keyphrase_ngram_range=(1, 2))
    query = keywords[0][0]
    googleAPIKey = '<YourGoogleAPIKey>'
    pages = wikipedia.search(query)
    res = json.loads(requests.get('https://www.googleapis.com/customsearch/v1?key={0}&cx=e06fb929e97c745ac&q={1}&searchType=image'.format(googleAPIKey, query)).content)
    images = []
    for item in res['items']:
        images.append(item['link'])
    text = ''
    titles = []
    for i in range(6):
        try:
            page = wikipedia.summary(pages[i])
            summ = summarizer(page)
            titles.append(pages[i])
            text += summ[0]['summary_text']
        except:
            continue
    return {
        'headings':[{'id':x, 'content':pages[x]} for x in range(len(pages))], 
        'content':text, 
        'images':[{'id':x, 'url':images[random.randint(0,len(images)-1)]} for x in range(3)]
    }

@app.route('/wordpress' , methods=["POST"])
def post():
    data = request.get_json()
    html = ""
    post = data['articleData']
    
    for item in post:
        if(item['type'] == 'IMAGE'):
            image_path = "temp.jpg"
            download_image(item['url'], image_path)
            files = {"file": open(image_path, "rb")}
            response_upload = requests.post(upload_url, headers=headers, files=files)
            if response_upload.status_code == 201:
                html += json.loads(requests.get(upload_url+str(response_upload.json().get("id"))).content)['description']['rendered']
            else:
                abort(400)
            
        if(item['type'] == 'TEXT'):
            html += "<p>{0}</p>".format(item['content'])
        
        if(item['type'] == 'HEADING'):
            html += "<h2>{0}</h2>".format(item['content'])
            
    url = wordpress_url + '?rest_route=/wp/v2/posts/'
    data = {
        'title': data['title'],
        'status': 'draft',
        'author': 1,
        'content': html,
    }

    # Send the HTTP request
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    # Check the response
    if response.status_code == 201:
        return 'Post created successfully'
    else:
        abort(500)

if __name__ == '__main__':
    app.run(debug=True)