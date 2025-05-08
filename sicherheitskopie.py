#erstellt eine Sicherheitskopie der gesamten Tabelle der Datenbank

import sys
import os
sys.path.append(os.path.abspath('.'))
from database import Database_postgres

# verbinde mit Database
database = Database_postgres("localhost","newspaper","postgres","1234",5432)
database.connect()
database.safety_copy("all_articles")
database.disconnect()