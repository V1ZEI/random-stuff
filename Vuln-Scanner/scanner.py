import requests
import re
from bs4 import BeautifulSoup
import urllib.parse as urlparse

class Scanner:
    def __init__(self, url, ignoreLinks):
        self.session = requests.Session()
        self.targetURL = url
        self.targetLinks = []
        self.ignoreLinks = ignoreLinks
        self.xss_test_script = "<sCript>alert('hello')</scriPt>"
    
    def extract_links_from(self, url):
        response = self.session.get(url)
        # return re.findall('(?:href=")(.*?)"', response.content)
        return re.findall('(?:href=")(.*?)"', str(response.content))
    
    def crawl(self, url=None):
        if url == None:
            url = self.targetURL
        hrefLinks = self.extract_links_from(url)
        for link in hrefLinks:
            link = urlparse.urljoin(url, link)
            if '#' in link:
                link = link.split("#")[0]
            if self.targetURL in link and link not in self.targetLinks and link not in self.ignoreLinks:
                self.targetLinks.append(link)
                print(link)
                self.crawl(link)
    
    def extract_forms(self, url):
        response = self.session.get(url)
        html_content = BeautifulSoup(response.content, 'html.parser')
        return html_content.findAll('form')
    
    def submit_form(self, form, value, url):
        action = form.get('action')
        post_url = urlparse.urljoin(url, action)
        print(post_url)
        method = form.get('method')
        inputs = form.findAll('input')
        post_data = {}
        for input in inputs:
            input_name = input.get('name')
            input_type = input.get('type')
            inputValue = input.get('value')
            if "text" in input_type:
                inputValue = value
            post_data[input_name] = inputValue
        if method.lower() == 'post':
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def start(self):
        for link in self.targetLinks:
            forms = self.extract_forms(link)
            for form in forms:
                print("[=] forms link -> " + str(link))
                xss_vuln = self.xss_in_form(form, link)
                if xss_vuln:
                    print("\n------ XSS VULN FOUND IN " + str(link) + " IN THE FORM-----------")
                    print()
                    print(form)
                    print("-------------------")
            
            if "=" in link:
                print("[=] Testing link: " + str(link))
                xss_vuln = self.xss_in_link(link)
                if xss_vuln:
                    print("\n----- XSS in link -> " + str(link))

    
    def xss_in_link(self, url):
        url = url.replace("=", "="+self.xss_test_script)
        response = self.session.get(url)
        return self.xss_test_script in response.content.decode()
    
    def xss_in_form(self, form, url):
        response = self.submit_form(form, self.xss_test_script, url)
        return self.xss_test_script in response.content.decode()