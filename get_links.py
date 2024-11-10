
from xhtml2pdf import pisa
from urllib.request import Request, urlopen
import re

def get_html(url):
    req = Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    print('HTML abgefragt  :  '+str(url))
    return html

def extract_links(html):
    pass


def get_all_html():
    link_of_list = []
    for i in range(1,1001):
        text = get_html("https://www.billboard.com/c/music/music-news/page/"+str(i)+"/")
        pattern = r"https://www\.billboard\.com/music/music-news/.+?/"
        for j in re.findall(pattern, text):
            link_of_list.append(j)

        link_of_list = list(dict.fromkeys(link_of_list))

    test = ""
    for i in link_of_list:
        test.join(i)
    print(test)

    a = open('list_of_links.txt', 'w', encoding="utf-8")
    a.write(str(link_of_list))
    a.close()

get_all_html()


#"https://www.billboard.com/music/music-news/zach-bryan-ex-brianna-lapaglia-alleges-emotional-abuse-rejects-12-million-nda-offer-1235823179/"