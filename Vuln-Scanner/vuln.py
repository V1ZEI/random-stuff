import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse


def request(url):
    try:
        return requests.get(url)
    except requests.exception.connectionError:
        pass

targetURL = "target_url"
response = request(targetURL)

# in python2 -> response.content is string 
# in python3 -> response.content is bytes
# print(response.content)

html_content = BeautifulSoup(response.content, 'html.parser')
forms = html_content.findAll('form')
for form in forms:
    action = form.get('action')
    post_url = urlparse.urljoin(targetURL, action)
    print(post_url)
    method = form.get('method')
    inputs = form.findAll('input')
    post_data = {}
    for input in inputs:
        input_name = input.get('name')
        input_type = input.get('type')
        inputValue = input.get('value')
        if "text" in input_type:
            inputValue = "test"
        post_data[input_name] = inputValue
    result = requests.post(post_url, data=post_data)
    print(result.content.decode())
# print(forms)