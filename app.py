from flask import Flask, request, redirect, render_template_string
import string
import random
from db import urls
import hashlib 
import re 

app = Flask(__name__)
app.config['BASE_URL'] = 'http://localhost:5000/'  


url_store = {}

def validate_and_correct_url(url):
    # Check if URL starts with http:// or https:// and www.
    if not re.match(r'^https?://www\.', url):
        # If not, try to correct it
        if url.startswith('www.'):
            corrected_url = 'https://' + url
        elif url.startswith('http://'):
            corrected_url = url.replace('http://', 'https://')
        elif url.startswith('https://'):
            corrected_url = url
        else:
            corrected_url = 'https://www.' + url
        return corrected_url
    return url


def generate_short_url(longURL):
    hash_object = hashlib.sha256(longURL.encode())
    hash_digest = hash_object.hexdigest()[:8]  
    return hash_digest


@app.route('/')
def index():
    return render_template_string('<form method="POST" action="/shorten">' 
                                  'Long URL: <input type="text" name="url">' 
                                  '<input type="submit" value="Shorten"></form>')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    validated_url = validate_and_correct_url(long_url)
    if not validated_url:
        return "Invalid URL format", 400

    short_url = generate_short_url(validated_url)
    absolute_url = f"{app.config['BASE_URL']}/{short_url}"

    if urls.find_one({'short_url':short_url}) :
         return render_template_string('Shortened URL: <a href="{{ url }}">{{ url }}</a>',
                                  url=absolute_url)

    urls.insert_one({'short_url': short_url, 'long_url': validated_url})
    return render_template_string('Shortened URL: <a href="{{ url }}">{{ url }}</a>',
                                  url=absolute_url)
@app.route('/<short_url>')
def redirect_to_url(short_url):
    long_url = urls.find_one({'short_url':short_url})['long_url']
    return redirect(long_url)

if __name__ == '__main__':
    app.run(debug=True)
