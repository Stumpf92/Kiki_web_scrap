from database import Database
import time
from weasyprint import HTML
import re

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
words = ['nda','ndas']
patter = r'(?i)(?:^|(?<= ))('+'|'.join(words) + ')(?:(?= )|$)'

mask = dataframe[['text','title']].apply(lambda x: x.str.contains(patter, regex=True).any(), axis=1)

filtered = dataframe[mask]

def markiere_woerter(html_text, woerter_liste):
    for wort in woerter_liste:
        # Regex für exakte Wortübereinstimmung (case-insensitive)
        html_text = re.sub(rf'\b({re.escape(wort)})\b', r'<mark>\1</mark>', html_text, flags=re.IGNORECASE)
    return html_text

heutiges_datum = time.strftime("%d.%m.%Y, %H:%M:%S")
first_html = f"""
<html>
<head>
    <style>
        @page {{
            size: A4;
            margin: 2cm;

            @bottom-center {{
                content: "Seite " counter(page) " von " counter(pages);
                font-family: Arial;
                font-size: 13pt;
                text-align: center;
            }}
        }}

        .page-content{{
            text-align: left;
            padding: 0px;
        }}

        .seitenumbruch {{
            page-break-before: always;
        }}
    </style>
</head>
<body>
    <div class="page-content">
        <p style="font-size: 20px; font-family: Arial; font-weight: bold; text-align: center">
        Report
        </p>
        <p style="font-size: 13px; font-family: Arial;">
        date: {heutiges_datum}
        </br>
        number of evaluated articles: {str(dataframe.shape[0])}
        </br>
        number of interesting articles: {str(len(filtered))}
        </br>
        filter by: {str(words)}
        </br>
        sorted by: highest number of matches first
        </p>
    </div>
    <div class="seitenumbruch"></div>
"""


# HTML für mehrere Seiten generieren (dies ist nur ein Beispiel, wie du mehrere Seiten erstellen könntest)
next_html = ""
for index, row in filtered.iterrows():  # Erstelle Seiten 1 bis 5
    url = str(row['url'])
    date = str(row['release_date'])
    titel = markiere_woerter(str(row['title']), words)
    text = markiere_woerter(str(row['text']), words)
    page_html = f"""
    <div class="page-content">
        <p style="font-size: 13px; font-family: Arial;">
        <a href="{url}">{url}</a>
        </p>
        <p style="font-size: 13px; font-family: Arial;">
        {date}
        </p>
        <p style="font-size: 15px; font-family: Arial; text-decoration: underline">
        {titel}
        </p>
        <p style="font-size: 13px; font-family: Arial;">
        {text}
        </p>
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
jetzt = str(round(time.time()))
HTML(string=complete_html).write_pdf(f"search_reports/{jetzt}_output.pdf")

print("PDF erfolgreich erstellt!")


db.disconnect()