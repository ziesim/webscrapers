import os
import time  # Bibliothek für Zeitfunktionalitäten
import re  # Bibliothek für reguläre Ausdrücke
import json  # Bibliothek zum Verarbeiten von JSON-Daten
from selenium import webdriver  # Selenium-Bibliothek für Webautomation
from selenium.webdriver.firefox.service import Service  # Service für den Geckodriver
from selenium.webdriver.common.by import By  # Selektoren für das Auffinden von Elementen
from selenium.webdriver.support.ui import WebDriverWait  # Warten auf Bedingungen
from selenium.webdriver.support import expected_conditions as EC  # Erwartete Bedingungen für Warten
from selenium.webdriver.firefox.options import Options  # Optionen für den Firefox-Browser

if os.path.exists("../data/Konzertdaten.txt"):
    os.remove("../data/Konzertdaten.txt")

# Laden der Bandliste aus der JSON-Datei
with open('../data/Bands.json') as json_file:
    data = json.load(json_file)

# Pfad zum Geckodriver angeben (abhängig von der Installation)
service = Service(executable_path='/usr/bin/geckodriver')

# Optionen für den Headless-Modus festlegen (unsichtbare Ausführung des Browsers)
options = Options()
options.headless = True  # Browser unsichtbar machen
options.add_argument("--headless")  # Weitere Option für Headless-Modus
options.add_argument("--disable-gpu")  # GPU deaktivieren, um Probleme zu vermeiden
options.add_argument("--window-size=1920,1200")  # Fenstergröße setzen, um Layoutprobleme zu vermeiden

# Webdriver mit den Optionen initialisieren (Firefox wird gestartet)
driver = webdriver.Firefox(service=service, options=options)
driver.get('https://www.stattbahnhof.de/')  # Webseite öffnen

# Warten, bis der Button für die Cookie-Akzeptanz sichtbar ist und dann klicken
accept_cookies_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@class="cmplz-btn cmplz-accept"]'))
)
accept_cookies_button.click()

# Initialisierung der Listen für die extrahierten Daten
all_bands = []  # Liste für alle Bandnamen aus der JSON-Datei
bands = []  # Liste für die gefundenen Bandnamen
dates = []  # Liste für die extrahierten Datumsangaben
weekdays = []  # Liste für die Wochentage
days = []  # Liste für die Tage
months = []  # Liste für die Monate
years = []  # Liste für die Jahre

# Wörterbuch für die Übersetzung von Monatsnamen ins Zahlenformat
complete_months = {
    "Januar": "01",
    "Februar": "02",
    "März": "03",
    "April": "04",
    "Mai": "05",
    "Juni": "06",
    "Juli": "07",
    "August": "08",
    "September": "09",
    "Oktober": "10",
    "November": "11",
    "Dezember": "12"
}

# Bandnamen aus der JSON-Datei in eine Liste formatieren
for band_data in data:
    band_name = band_data["bands"]
    all_bands.extend(band_name)

# Funktion zur Umwandlung des Monatsnamens in die Monatsnummer
def month_to_int(monat_name):
    return complete_months.get(monat_name.title())


# Schleife für das Laden zusätzlicher Inhalte auf der Webseite (3 Mal)
count = 1
while count <= 3:
    # "Mehr laden"-Button finden und klicken
    initial_load_more_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/main/div/div/div/div/div/section[1]/div/div/div/div/div/div/div/div[4]/div'))
    )
    initial_load_more_button.click()

    time.sleep(5)  # Warten, um sicherzustellen, dass die Inhalte geladen werden
    count += 1

# Titel der Events sammeln
get_all_bands = driver.find_elements(By.CLASS_NAME, 'mec-color-hover')  # Alle Event-Titel finden
get_all_dates = driver.find_elements(By.CLASS_NAME, 'mec-start-date-label')  # Alle Event-Datumsangaben finden

# Liste der Event-Titel aktualisieren
for title in get_all_bands:
    if "Tickets" not in title.text and title.text:  # Ausschluss von "Tickets"-Einträgen
        text = title.text.lower()

        gefunden = False
        # Überprüfen, ob der Bandname in der Liste aller Bands enthalten ist
        for band_name in all_bands:
            if re.search(rf"\b{band_name}\b", text):  # Treffer am Wortanfang/Ende
                gefunden = True
                break

        if gefunden:
            bands.append(title.text)  # Bandnamen zur Liste hinzufügen
        else:
            bands.append("Uninteressant")  # Für uninteressante Bands "Uninteressant" zur Liste hinzufügen

# Extrahieren und Aufbereiten der Datumsangaben
for date in get_all_dates:
    if date.text:  # Sicherstellen, dass ein Datum vorhanden ist
        pattern = r"(\w+), (\d+)\. (\w+) (\d+)"  # Muster für alle Komponenten definieren
        match = re.search(pattern, date.text)  # Übereinstimmung mit dem Muster suchen
        if match:
            weekday = match.group(1)  # Wochentag extrahieren
            day = match.group(2)  # Datum extrahieren
            month = match.group(3)  # Monat extrahieren
            year = match.group(4)  # Jahr extrahieren

            weekdays.append(weekday[:2])  # Wochentag (Abkürzung) zur Liste hinzufügen
            if len(day) == 1:
                day = "0" + day  # Führende Null hinzufügen, falls der Tag einstellig ist
            days.append(day)  # Tag zur Liste hinzufügen

            month = month_to_int(month)  # Monat in Nummer umwandeln
            months.append(month)  # Monat zur Liste hinzufügen

            years.append(year)  # Jahr zur Liste hinzufügen

datei = open('../data/Konzertdaten.txt', 'w')

# Ausgabe der finalen Ergebnisse
print("")
print("STATTBAHNHOF SCHWEINFURT:")
datei.write("STATTBAHNHOF SCHWEINFURT:\n")

# Ausgabe der formatierten Konzertdaten
for weekday, day, month, year, band in zip(weekdays, days, months, years, bands):
    if "Uninteressant" not in band:  # Filtern von "Uninteressant"-Bands
        print(f"{weekday}   {day}.{month}.{year}   {band.title()}")
        datei.write(f"{weekday}   {day}.{month}.{year}   {band.title()}\n")

datei.write("\n")

# Webdriver schließen
driver.quit()

datei.write("")
