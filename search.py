from database import Database_postgres
import time
from weasyprint import HTML
import re
from ai import Ai
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import base64
from PIL import Image
from io import BytesIO


def generate_wordcloud(huge_text):
    wc = None 
    wc = WordCloud(width=600, height=600, background_color='white', stopwords=STOPWORDS, max_words=300, min_word_length=3 )
    wc.generate(huge_text)
    with open("temp/wordcloud.txt", "w", encoding="utf-8") as f:
        f.write(str(huge_text))
    wc.to_file("temp/wordcloud.png")
    print("wordcloud erstellt")

    return wc

def markiere_woerter(html_text, woerter_liste):
    for wort in woerter_liste:
        # Regex für exakte Wortübereinstimmung (case-insensitive)
        html_text = re.sub(rf'\b({re.escape(wort)})\b', r'<mark>\1</mark>', html_text, flags=re.IGNORECASE)
    return html_text

def safe_int(k):
    try:
        return int(k)  # Versuche, k in eine Zahl umzuwandeln
    except (ValueError, TypeError):
        return None  # Falls es fehlschlägt, gib None zurück


db_postgres = Database_postgres("localhost","newspaper","postgres","1234",5432)
#psycopg2.connect(host=self.host, dbname=self.db_name, user=self.user, password=self.password, port=self.port)
db_postgres.connect()

ai_mode = False
# model = "deepseek-llm"
if ai_mode:
    model = "llama3.1"
    seed = 42
    ai = Ai(model, seed)


table = 'all_articles'
columns = [['source','TEXT'],
           ['url','TEXT'],
           ['author','TEXT'],
           ['release_date','TEXT'],
           ['title','TEXT'],
           ['text','TEXT'],
           ['import_time','TEXT'],
           ['id','TEXT']]


# load all data into dataframe
dataframe = db_postgres.synch(table, columns)
# dataframe = dataframe.sample(frac=1, random_state=seed).reset_index(drop=True)
# dataframe = dataframe.head(10000)
print("Datenbank geladen")



# white_list = ['nda', 'ndas', "nda's"]
# white_list = ['confidential', 'confidentiality', 'in confidence','secret', 'secrets', 'secrecy', 'secretive',
#                'nda', 'ndas', "nda's", 'non disclosure', 'non-disclosure', 'nondisclosure', 'non disclosures', 'non-disclosures', 'nondisclosures' ,
#                 'disclose', ' disclosed' , 'disclosing', 'discloses', 'disclosure', 'disclosures', 'discloseable', 'disclosable', 'discloser', 'disclosers', 'disclosing party', 'disclosing parties', 'disclosed party', 'disclosed parties',
#                 'leak', 'leaks', 'leaked', 'leaking', 'leakage', 'leakages',
#                 'breach', 'breaches', "breach's", 'breaching', 'breachings'
#                 ]

white_list = ['confidential', 'confidentiality', 'in confidence','secret', 'secrets', 'secrecy', 'secretive',
               'nda', 'ndas', "nda's", 'non disclosure', 'non-disclosure', 'nondisclosure', 'non disclosures', 'non-disclosures', 'nondisclosures'
                ]

# black_list = ['revealed he an NDA']
black_list = ['If you or someone you know has experienced sexual abuse, call the National Sexual Assault Hotline at 800-656-4673 for confidential help 24/7',
              'website for free, confidential emotional support and resources 24/7',
              'If you or someone you know is a victim of domestic violence, please call the confidential National Domestic Violence Hotline toll-free at 1-800-799-7233, or go to thehotline.org.',
              'Stories about sexual assault allegations can be traumatizing for survivors of sexual assault. If you or anyone you know needs support, you can reach out to the Rape, Abuse & Incest National Network (RAINN). The organization provides free, confidential support to ',
              'If you or someone you know has experienced sexual violence and need support and/or resources, reach out to RAINN and the National Sexual Assault Hotline (800-656-HOPE) for free, confidential help 24/7',
              'If you or anyone you know is experiencing suicidal thoughts, call 988 for the Suicide and Crisis Lifeline for free, confidential support 24/7.',
              '24/7 National Sexual Assault Hotline here for confidential support and resources.',
              'Sexual Assault Hotline at 800-656-4673 or chat at online.rainn.org 24/7 for confidential support.',
              'If you or anyone you know needs help with substance abuse, reach out to the Substance Abuse and Mental Health Services Administration for confidential help and resources 24/7.',
              'If you or anyone you know is experiencing suicidal ideation, reach out to the National Suicide Prevention Lifeline at 1-800-273-8255 (or dial 988) for free, confidential support 24/7',
              'If you or someone you know is in need of mental health services, reach out to SAMHSA for free and confidential information on mental health resources, treatment and more 24/7 at samhsa.gov or 1-800-662-HELP (4357)/',
              'If you or anyone you know is experiencing suicidal thoughts, reach out to the National Suicide Prevention Lifeline (1-800-273-8255, or dial 988) for free, confidential support and resources 24/7',
              'If you or anyone you know has been sexually assaulted, reach out to RAINN for confidential support and resources from a trained staff member.',
              ]


white_list_regex = []
for wort in white_list:
    white_list_regex.append(r'\b' + re.escape(wort) + r'\b')


whitelist_pattern = '|'.join(white_list_regex)
blacklist_pattern = '|'.join(re.escape(satz) for satz in black_list)

suchrelevante_spalten = ['text','title']
mask = False
for spalte in suchrelevante_spalten:
    # Find all whitelist matches
    whitelist_matches = dataframe[spalte].str.findall(whitelist_pattern, flags=re.IGNORECASE)
    
    # For each row, check if any whitelist match is part of a blacklist phrase
    def check_blacklist(text, matches):
        if not matches:  # No whitelist matches
            return False
        text_lower = text.lower()
        for match in matches:
            # Check if this whitelist match is part of any blacklist phrase
            for black_phrase in black_list:
                if match.lower() in black_phrase.lower():
                    # If the whitelist match is part of a blacklist phrase, check if the full blacklist phrase is present
                    if black_phrase.lower() in text_lower:
                        return False
        return True  # No blacklist conflicts found
    
    # Apply the check to each row
    mask = mask | dataframe.apply(lambda row: check_blacklist(row[spalte], whitelist_matches[row.name]), axis=1)

filtered = dataframe[mask]
print("Datenbank nach Suchwörtern durchsucht")
print(filtered.shape)



if ai_mode:
    questions_answers = [['is there a legal conflict in the following text, return only "yes" or "no"'],
                         
                        ]

years_billboard = {}
years_music_business_world_wide = {}
years_rolling_stone = {}
years_variety = {}
noa_billboard = 0
noa_music_business_world_wide = 0
noa_rolling_stone = 0
noa_variety = 0
length_list = []
for index, row in dataframe.iterrows():
    year = row['release_date'].split('-')[0]
    length_list.append(len(list(row["title"]))+len(list(row["text"])))
    if row['source'] == 'BILLBOARD':
        noa_billboard += 1
        if year in years_billboard:
            years_billboard[year] += 1
        else:
            years_billboard[year] = 1
    elif row['source'] == 'MUSIC_BUSINESS_WORLD_WIDE':
        noa_music_business_world_wide += 1
        if year in years_music_business_world_wide:
            years_music_business_world_wide[year] += 1
        else:
            years_music_business_world_wide[year] = 1
    elif row['source'] == 'ROLLING_STONE':
        noa_rolling_stone += 1
        if year in years_rolling_stone:
            years_rolling_stone[year] += 1
        else:
            years_rolling_stone[year] = 1
    elif row['source'] == 'VARIETY':
        noa_variety += 1
        if year in years_variety:
            years_variety[year] += 1
        else:    
            years_variety[year] = 1

years_billboard_filtered = {}
years_music_business_world_wide_filtered = {}
years_rolling_stone_filtered = {}
years_variety_filtered = {}
noa_billboard_filtered = 0
noa_music_business_world_wide_filtered = 0
noa_rolling_stone_filtered = 0
noa_variety_filtered = 0
all_text_filtered = ''
length_list_filtered = []
for index, row in filtered.iterrows():
    year = row['release_date'].split('-')[0]
    length_list_filtered.append(len(list(row["title"]))+len(list(row["text"])))
    all_text_filtered += row['text']
    all_text_filtered += row['title']
    if row['source'] == 'BILLBOARD':
        noa_billboard_filtered += 1
        if year in years_billboard_filtered:
            years_billboard_filtered[year] += 1
        else:
            years_billboard_filtered[year] = 1
    elif row['source'] == 'MUSIC_BUSINESS_WORLD_WIDE':
        noa_music_business_world_wide_filtered += 1
        if year in years_music_business_world_wide_filtered:
            years_music_business_world_wide_filtered[year] += 1
        else:
            years_music_business_world_wide_filtered[year] = 1
    elif row['source'] == 'ROLLING_STONE':
        noa_rolling_stone_filtered += 1
        if year in years_rolling_stone_filtered:
            years_rolling_stone_filtered[year] += 1
        else:
            years_rolling_stone_filtered[year] = 1
    elif row['source'] == 'VARIETY':
        noa_variety_filtered += 1
        if year in years_variety_filtered:
            years_variety_filtered[year] += 1
        else:    
            years_variety_filtered[year] = 1


wc = generate_wordcloud(all_text_filtered)
with open("temp/wordcloud.png", "rb") as image_file:
    encoded_string_wordcloud = base64.b64encode(image_file.read()).decode('utf-8')

# Kuchendiagramm für alle Artikel
labels = ["Billboard", "Music Business World Wide", "Rolling Stone", "Variety"]
values = [noa_billboard, noa_music_business_world_wide, noa_rolling_stone, noa_variety]
plt.figure(figsize=(7,5))  
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  
plt.title(f'Verteilung aller Artikel, Gesamtanzahl: {noa_billboard + noa_music_business_world_wide + noa_rolling_stone + noa_variety}')
plt.savefig('temp/kuchendiagramm_alle_artikel.png', dpi=500, bbox_inches='tight')
img = Image.open('temp/kuchendiagramm_alle_artikel.png')
img_resized = img.resize((350, 250), Image.LANCZOS) 
buffer = BytesIO()
img_resized.save(buffer, format="PNG")
encoded_string_kuchendiagramm_alle_artikel = base64.b64encode(buffer.getvalue()).decode('utf-8')


# Kuchendiagramm für gefilterte Artikel
labels = ["Billboard", "Music Business World Wide", "Rolling Stone", "Variety"]
values = [noa_billboard_filtered, noa_music_business_world_wide_filtered, noa_rolling_stone_filtered, noa_variety_filtered]
plt.figure(figsize=(7,5))  
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  
plt.title(f'Verteilung aller Artikel, Gesamtanzahl: {noa_billboard_filtered + noa_music_business_world_wide_filtered + noa_rolling_stone_filtered + noa_variety_filtered}')
plt.savefig('temp/kuchendiagramm_gefilterte_artikel.png', dpi=500, bbox_inches='tight')
img = Image.open('temp/kuchendiagramm_gefilterte_artikel.png')
img_resized = img.resize((350, 250), Image.LANCZOS) 
buffer = BytesIO()
img_resized.save(buffer, format="PNG")
encoded_string_kuchendiagramm_gefilterte_artikel = base64.b64encode(buffer.getvalue()).decode('utf-8')


# Liniendiagramm jährliche Verteilung aller Artikel
all_keys = sorted(
    safe_int(k) for k in (
        set(years_billboard.keys()) |
        set(years_music_business_world_wide.keys()) |
        set(years_rolling_stone.keys()) |
        set(years_variety.keys())
    )
    if safe_int(k) is not None and 1990 <= safe_int(k) <= 2025
)
# Fehlende Werte mit None oder einem Platzhalter ersetzen
y1 = [years_billboard.get(str(k), None) for k in all_keys]
y2 = [years_music_business_world_wide.get(str(k), None) for k in all_keys]
y3 = [years_rolling_stone.get(str(k), None) for k in all_keys]
y4 = [years_variety.get(str(k), None) for k in all_keys]
# Plot erstellen
plt.figure(figsize=(7,5))  
plt.plot(all_keys, y1, marker='o', linestyle='-', label="Billboard", color='b')
plt.plot(all_keys, y2, marker='o', linestyle='-', label="Music Business World Wide", color='r')
plt.plot(all_keys, y3, marker='o', linestyle='-', label="Rolling Stone", color='g')
plt.plot(all_keys, y4, marker='o', linestyle='-', label="Variety", color='y')
plt.xticks(all_keys[::5])
plt.xlim(1990, 2025)
# Diagramm formatieren
plt.xlabel("Jahr")
plt.ylabel("Anzahl")
plt.title("Anzahl der Artikel pro Jahr")
plt.legend()
plt.grid(True)
plt.savefig('temp/liniendiagramm_alle_artikel.png', dpi=500, bbox_inches='tight')
img = Image.open('temp/liniendiagramm_alle_artikel.png')
img_resized = img.resize((350, 250), Image.LANCZOS) 
buffer = BytesIO()
img_resized.save(buffer, format="PNG")
encoded_string_liniendiagramm_alle_artikel = base64.b64encode(buffer.getvalue()).decode('utf-8')

# Liniendiagramm jährliche Verteilung aller Artikel
all_keys = sorted(
    safe_int(k) for k in (
        set(years_billboard_filtered.keys()) |
        set(years_music_business_world_wide_filtered.keys()) |
        set(years_rolling_stone_filtered.keys()) |
        set(years_variety_filtered.keys())
    )
    if safe_int(k) is not None and 1990 <= safe_int(k) <= 2025
)
# Fehlende Werte mit None oder einem Platzhalter ersetzen
y1 = [years_billboard_filtered.get(str(k), None) for k in all_keys]
y2 = [years_music_business_world_wide_filtered.get(str(k), None) for k in all_keys]
y3 = [years_rolling_stone_filtered.get(str(k), None) for k in all_keys]
y4 = [years_variety_filtered.get(str(k), None) for k in all_keys]
plt.figure(figsize=(7,5))  
plt.plot(all_keys, y1, marker='o', linestyle='-', label="Billboard", color='b')
plt.plot(all_keys, y2, marker='o', linestyle='-', label="Music Business World Wide", color='r')
plt.plot(all_keys, y3, marker='o', linestyle='-', label="Rolling Stone", color='g')
plt.plot(all_keys, y4, marker='o', linestyle='-', label="Variety", color='y')
plt.xticks(all_keys[::2])
# Diagramm formatieren
plt.xlabel("Jahr")
plt.ylabel("Anzahl")
plt.title("Anzahl der gefilterten Artikel pro Jahr")
plt.legend()
plt.grid(True)
plt.savefig('temp/liniendiagramm_gefilterte_artikel.png', dpi=500, bbox_inches='tight')
img = Image.open('temp/liniendiagramm_gefilterte_artikel.png')
img_resized = img.resize((350, 250), Image.LANCZOS) 
buffer = BytesIO()
img_resized.save(buffer, format="PNG")
encoded_string_liniendiagramm_gefilterte_artikel = base64.b64encode(buffer.getvalue()).decode('utf-8')

#histogramm für ungefähre Wortverteilung im gesamten set und im gefilterten set
plt.figure(figsize=(7,5))  
plt.hist(length_list, bins=100)
plt.ylabel("Anzahl der Wörter")
plt.title("Verteilung des gesamten Sets")
plt.savefig('temp/histogramm_artikel.png', dpi=500, bbox_inches='tight')
img = Image.open('temp/histogramm_artikel.png')
img_resized = img.resize((350, 250), Image.LANCZOS) 
buffer = BytesIO()
img_resized.save(buffer, format="PNG")
encoded_string_histogramm_artikel = base64.b64encode(buffer.getvalue()).decode('utf-8')

plt.figure(figsize=(7,5))  
plt.hist(length_list_filtered, bins=100)
plt.ylabel("Anzahl der Wörter")
plt.title("Verteilung des gefilterten Sets")
plt.savefig('temp/histogramm_gefilterte_artikel.png', dpi=500, bbox_inches='tight')
img = Image.open('temp/histogramm_gefilterte_artikel.png')
img_resized = img.resize((350, 250), Image.LANCZOS) 
buffer = BytesIO()
img_resized.save(buffer, format="PNG")
encoded_string_histogramm_gefilterte_artikel = base64.b64encode(buffer.getvalue()).decode('utf-8')




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
        .center-image {{
            text-align: center;
            margin: 0 auto;
        }}
        
        img {{
            display: block;
            margin-left: auto;
            margin-right: auto;
        }}
        .image-container {{
            display: flex;
            justify-content: center;
            gap: 20px; /* Abstand zwischen den Bildern */
            margin: 20px 0;
        }}

        .image-item {{
            flex: 1;
            max-width: 48%; /* Verhindert, dass die Bilder zu breit werden */
        }}

        .image-item img {{
            width: 100%;
            height: auto;
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
        whitelist: {str(white_list)}
        </br>
        blacklist: {str(black_list)}
        </br>"""
if ai_mode:
    first_html += f"""
            AI used for analisys: {str(model)}
            Seed : {str(seed)}
            </br>"""
if ai_mode:
    for counter, content in enumerate(questions_answers):
        first_html += f"""
                {str(counter +1)} Question: {str(content[0])}
                </br>"""

first_html += f"""
            </br>
            <div class="image-container">
                <div class="image-item">
                    <img src="data:image/png;base64,{encoded_string_kuchendiagramm_alle_artikel}">
                </div>
                <div class="image-item">
                    <img src="data:image/png;base64,{encoded_string_kuchendiagramm_gefilterte_artikel}">
                </div>
            </div>
            <div class="image-container">
                <div class="image-item">
                    <img src="data:image/png;base64,{encoded_string_liniendiagramm_alle_artikel}">
                </div>
                <div class="image-item">
                    <img src="data:image/png;base64,{encoded_string_liniendiagramm_gefilterte_artikel}">
                </div>
            </div>
            <div class="image-container">
                <div class="image-item">
                    <img src="data:image/png;base64,{encoded_string_histogramm_artikel}">
                </div>
                <div class="image-item">
                    <img src="data:image/png;base64,{encoded_string_histogramm_gefilterte_artikel}">
                </div>
            </div>
            </br>
            <div class="center-image">
                <img src="data:image/png;base64,{encoded_string_wordcloud}">
            </div>
            </br>
            </br>
    """
first_html += f"""
        </p>
    </div>
    <div class="seitenumbruch"></div>
"""


# HTML für mehrere Seiten generieren (dies ist nur ein Beispiel, wie du mehrere Seiten erstellen könntest)
next_html = ""
for index, row in filtered[:].iterrows():
    url = str(row['url'])
    date = str(row['release_date'])
    titel = markiere_woerter(str(row['title']), white_list)
    text = markiere_woerter(str(row['text']), white_list)
    length = len(list(titel)) + len(list(text))
    page_html = f"""
    <div class="page-content">
        <p style="font-size: 13px; font-family: Arial;">
        <a href="{url}">{url}</a>
        </p>
        <p style="font-size: 13px; font-family: Arial;">
        Länge:  {str(length)}
        </p>
        <p style="font-size: 13px; font-family: Arial;">
        {date}
        </p>
        <p style="font-size: 15px; font-family: Arial; text-decoration: underline">
        {titel}
        </p>
        <p style="font-size: 13px; font-family: Arial;">
        {text}
        </p>"""
    if ai_mode:
        for _ in questions_answers:
            question = _[0]
            response= ai.prompt(question+row['text'])
            page_html += f""""
            <p style="font-size: 13px; font-family: Arial; text-decoration: underline">
            {question}
            </p>
            <p style="font-size: 13px; font-family: Arial;">
            {response}
            </p>"""
        
    page_html += f"""
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


db_postgres.disconnect()