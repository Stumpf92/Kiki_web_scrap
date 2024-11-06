
from xhtml2pdf import pisa
from urllib.request import Request, urlopen

#url = "http://olympus.realpython.org/profiles/poseidon"

#page = urlopen(url)


req = Request(
    url = "https://apitemplate.io/blog/how-to-convert-html-to-pdf-using-python/", 
    headers={'User-Agent': 'Mozilla/5.0'}
)
page = urlopen(req)
html = page.read().decode("utf-8")

print(html)

a = open('result.txt', 'w')
a.write(html)
a.close()

with open('result.pdf', "wb") as pdf_file:
    pisa_status = pisa.CreatePDF(html, dest=pdf_file)        



