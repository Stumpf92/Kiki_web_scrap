import datetime
import os

class Articles:    

    def __init__(self, db):
        self.all_articles = []
        self.update(db)

    def update(self, db):
        self.all_articles = []
        for row in range(db.data.shape[0]):
            Article(db.iloc[row]['source'],
                    db.iloc[row]['url'],
                    db.iloc[row]['author'],
                    db.iloc[row]['release_date'],
                    db.iloc[row]['title'],
                    db.iloc[row]['text'],
                    db.iloc[row]['tags'],
                    db.iloc[row]['import_time'],
                    db.iloc[row]['id']
                    )
            self.all_articles.append(Article)

    def get_articles_by_list(self, list):
        res = []
        for single in self.all_articles:
            if int(single.id) in list:
                res.append(single)

        return res
    
    def print_pdf(self, list):
        # CREATE A FOLDER
        timecode = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
        if not os.path.exists(timecode):
            os.makedirs(timecode)

        # PRINT EACH ELEMENT OF LIST
        for i in list:
            i.print_pdf(timecode)

    def print_info(self, list):
        for i in list:
            i.print_info()

    def filter(self, list):
        pass


class Article:

    def __init__(self, source, url, author, release_date, title, text, tags, import_time, id):
        self.source = source
        self.url = url
        self.author = author
        self.release_date = release_date
        self.title = title
        self.text = text
        self.tags = tags
        self.import_time = import_time
        self.id = id 

    def print_pdf(self, timecode):
        file_name = f"{timecode}/{self.id}.pdf"
        print("print_PDF_TBA")
        #https://www.geeksforgeeks.org/convert-text-and-text-file-to-pdf-using-python/

    def print_info(self):
        print("ID:   " + self.source + "\n")
        print("URL:   " + self.url + "\n")
        print("AUTHOR:   " + self.author + "\n")
        print("RELEASE_DATE:   " + self.release_date + "\n")
        print("TITLE:   " + self.title + "\n")
        print("TEXT:   " + self.text + "\n")
        print("TAGS:   " + self.tags + "\n")
        print("IMPORT_TIME:   " + self.import_time + "\n")






