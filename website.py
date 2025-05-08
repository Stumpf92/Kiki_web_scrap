from urllib.request import Request, urlopen


class Website:

    def __init__(self, url):
        self.url = url
    
    def get_html(self):
        html = None
        try:            
            print('HTML abgefragt  :  '+str(self.url))
            req = Request(
                    self.url, 
                    headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req)
            html = page.read().decode("utf-8")
        except: 
            "hupsi"
        return html
