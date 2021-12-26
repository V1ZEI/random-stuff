import scanner

url = "url"
linkToIgnore = ["url_to_ignore"]
data_dict = {'data': 'value', 'data1': 'value1'}

vulnS = scanner.Scanner(url, linkToIgnore)
vulnS.session.post("login_url", data=data_dict)
vulnS.crawl()
vulnS.start()