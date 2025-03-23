from database import Database
import time
# from xhtml2pdf import pisa
from weasyprint import HTML

db = Database("localhost","postgres","postgres","dfgtzu88",5432)
db.connect()

table = 'all_articles'
columns = [['article_id','INT'],
           ['source','TEXT'],
           ['url','TEXT'],
           ['author','TEXT'],
           ['release_date','TEXT'],
           ['title','TEXT'],
           ['text','TEXT'],
           ['tags','TEXT'],
           ['import_time','TEXT'],
            ['matches','TEXT']]


# load all data into dataframe
dataframe = db.synch(table, columns)

# declare a pattern
# words = ['nda','ndas','disclosure','confidentiality','confidential','disclosed','undisclosed','secret','contract']
words = ['hitler']
patter = r'(?i)(?:^|(?<= ))('+'|'.join(words) + ')(?:(?= )|$)'

mask = dataframe[['text','title']].apply(lambda x: x.str.contains(patter, regex=True).any(), axis=1)

filtered = dataframe[mask]

test = filtered[:5]


# # create html
# all_html = []

# # 1st page
# all_html.append("<html lang=\"de\"><head><style>@page { size: A4; margin: 2cm; @frame footer_frame { -pdf-frame-content: footer_content; bottom: 10px; height: 50px; } }.seitenumbruch { page-break-before: always; }</style></head>")
# all_html.append("<html><body>")
# all_html.append("<p>")
# all_html.append("REPORT")
# all_html.append("</p>")
# heutiges_datum = time.strftime("%d.%m.%Y")
# all_html.append("<p>")
# all_html.append("date: " + str(heutiges_datum))
# all_html.append("<br>")
# all_html.append("number of evaluated articles: " + str(dataframe.shape[0]))
# all_html.append("<br>")
# all_html.append("number of interesting articles: " + str(len(filtered)))
# all_html.append("<br>")
# all_html.append("used filter: " + str(words))
# all_html.append("</p>")
# all_html.append("<div id=\"footer_content\"> Seite <pdf:page> von <pdf:pageCount> </div>")
# all_html.append("<div class=\"seitenumbruch\"></div>")

# # next pages
# all_html.append("<p>")
# all_html.append("REPORT")
# all_html.append("</p>")
# heutiges_datum = time.strftime("%d.%m.%Y")
# all_html.append("<p>")
# all_html.append("date: " + str(heutiges_datum))
# all_html.append("<br>")
# all_html.append("number of evaluated articles: " + str(dataframe.shape[0]))
# all_html.append("<br>")
# all_html.append("number of interesting articles: " + str(len(filtered)))
# all_html.append("<br>")
# all_html.append("used filter: " + str(words))
# all_html.append("</p>")



# overview = []
# overview.append("<html><body>")
# for row in filtered:
#     overview.append("<p>")
#     overview.append("<a href=")
#     overview.append(row["url"])
#     overview.append(">")
#     overview.append(row.url)
#     overview.append("</a>")
#     overview.append("</p>")
#     overview.append("<p>")
#     overview.append('Release_date:   ')
#     overview.append(str(row.release_date))
#     overview.append("</p>")
#     overview.append("<p>")
#     overview.append('Artikel_id:   ')
#     overview.append(str(row.article_id))
#     overview.append("</p>")
#     overview.append("<p>")
#     overview.append('Filter:   ')
#     overview.append(str(filter_list))
#     overview.append("</p>")
#     overview.append("<p>")
#     overview.append('Number of Matches:   ')
#     overview.append(str(row.number_of_matches))
#     overview.append("</p>")
#     overview.append("<p><u>")
#     overview.append(str(row.title))
#     overview.append("</u></p>")
#     overview.append("<p>")
#     overview.append(str(row.text))
#     overview.append("</p>")
#     overview.append("<p>")
#     overview.append('TAGS:   ')
#     overview.append(str(row.tags))
#     overview.append("</p>")
#     overview.append("<br> </br>")
#     overview.append("<br> </br>")
#     overview.append("<br> </br>")
# overview.append("</body></html>")



# html = "".join(overview)
# for word in filter_list:
#     fil = "\\b"+word+"\\b"
#     sub = "<b>"+word+"</b>"
#     print (fil, "     ", sub)
#     html = re.sub(fil, sub, html, flags= re.I)

# complete_html = "".join(all_html)
# with open('test.txt', 'w',  encoding="utf-8") as a:
#     a.write(complete_html)
#     a.close()


# with open ("test.pdf", "w+b") as result_file:
#     pisa.CreatePDF(complete_html, dest= result_file)

# HTML mit Styles für Seitenzahlen und Seitenumbrüche
first_html = """
<html>
<head>
    <style>
        @page {
            size: A4;
            margin: 2cm;

            /* Seitenzahlen in der Mitte der Fußzeile */
            @bottom-center {
                content: "Seite " counter(page) " von " counter(pages);
            }
        }

        /* Zentrierter Text auf der Seite */
        body {
            margin: 0;
            font-family: Arial, sans-serif;
        }

        .page-content {
            text-align: center;
            padding: 50px;
        }

        .seitenumbruch {
            page-break-before: always; /* Erzwingt einen Seitenumbruch */
        }
    </style>
</head>
<body>
"""

# HTML für mehrere Seiten generieren (dies ist nur ein Beispiel, wie du mehrere Seiten erstellen könntest)
next_html = ""
for i in range(1, 6):  # Erstelle Seiten 1 bis 5
    page_html = f"""
    <div class="page-content">
        <h1>PDF mit Seitenzahlen</h1>
        <p>Dies ist Seite {i}</p>
    </div>
    <div class="seitenumbruch"></div>
    """
    next_html += page_html

# Das schließende HTML-Tag
last_html = """
</body>
</html>
"""

# Das vollständige HTML zusammenstellen
complete_html = first_html + next_html + last_html

# Das HTML in eine PDF-Datei umwandeln
HTML(string=complete_html).write_pdf("output.pdf")

print("PDF erfolgreich erstellt!")






db.disconnect()