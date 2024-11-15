from urllib.request import Request, urlopen
import re

def get_html(url):
    print('HTML abgefragt  :  '+str(url))
    req = Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    return html



html = get_html("https://www.billboard.com/sitemap_index.xml")
pattern= "<loc>(.*?)</loc>"
list = re.findall(pattern, html)


super_list = []
for i in list:
    super_list.append(get_html(i))

super_text = "".join(super_list)
pattern2= "https://www.billboard.com/music/music-news(.*?)</loc>"
final_list = re.findall(pattern2, super_text)

print("Anzahl der Links:   ", len(final_list))

a = open('final_links.txt', 'w',  encoding="utf-8")
for i in final_list:
    a.write("https://www.billboard.com/music/music-news"+str(i)+"\n")
a.close()

