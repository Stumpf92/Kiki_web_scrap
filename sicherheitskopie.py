#erstellt eine Sicherheitskopie der gesamten Tabelle der Datenbank

import sys
import os
sys.path.append(os.path.abspath('.'))
from database import Database

# verbinde mit Database
database = Database("localhost","postgres","postgres","dfgtzu88",5432)
database.connect()
database.safety_copy("all_articles")
database.disconnect()