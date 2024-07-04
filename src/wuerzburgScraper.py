from bs4 import BeautifulSoup  # Bibliothek zum Parsen von HTML
import requests  # Bibliothek für HTTP-Anfragen
import re  # Bibliothek für reguläre Ausdrücke
import json  # Bibliothek zum Verarbeiten von JSON-Daten
import datetime  # Bibliothek für die Arbeit mit Datum und Uhrzeit

# Laden der Bandliste aus der JSON-Datei
with open('../data/Bands.json') as json_file:
    data = json.load(json_file)

# Ziel-URL definieren, von der die Konzertdaten abgerufen werden sollen
website = 'https://posthalle.de/programm/'

# Abrufen des HTML-Inhalts der Website
result = requests.get(website)
content = result.text

# HTML-Inhalt der Webseite mit BeautifulSoup parsen
soup = BeautifulSoup(content, 'lxml')

# Den Container mit den Konzertinformationen anhand der CSS-Klasse finden
box = soup.find('div', class_='view-content')

# Initialisierung der erforderlichen Listen für die extrahierten Daten
all_bands = []  # Liste für alle Bandnamen aus der JSON-Datei
weekdays = []  # Liste für Wochentage (deutsch)
dates = []  # Liste für Datumstage (Tag)
days = []  # Liste für Tage (Tag)
bands = []  # Liste für Bandnamen
months = []  # Liste für Monate (Monat)
years = []  # Liste für Jahre (Jahr)
final_data = []  # Endgültige Liste für Kombination der Daten

# Datumsformat, das für die Konvertierung verwendet wird (Tag.Monat.Jahr)
date_format = "%d.%m.%Y"

# Wörterbuch für die Übersetzung von englischen Wochentagsabkürzungen ins Deutsche
english_to_german_weekdays = {
    "Mo": "Mo",
    "Tu": "Di",
    "We": "Mi",
    "Th": "Do",
    "Fr": "Fr",
    "Sa": "Sa",
    "Su": "So"
}

# Alle Bandnamen aus der JSON-Datei extrahieren und in eine Liste einfügen
for band_data in data:
    band_name = band_data["bands"]
    all_bands.extend(band_name)

# Durchlaufen der Konzert-Teaser im Container
for div in box.find_all('div', class_='tease-text'):
    # Extrahieren des Bandnamens aus der Überschrift
    for header in (div.find_all('h2')):
        for span in (header.find_all('span')):
            text = span.get_text().lower()

            gefunden = False
            # Überprüfen, ob der Bandname in der Liste aller Bands enthalten ist
            for band_name in all_bands:
                if re.search(rf"\b{band_name}\b", text):  # Treffer am Wortanfang/Ende
                    gefunden = True
                    break

            # Entsprechend der Überprüfung den Bandnamen zur Liste hinzufügen oder "Uninteressant" einfügen
            if gefunden:
                bands.append(span.get_text().title())  # Bandnamen großgeschrieben zur Liste hinzufügen
            else:
                bands.append("Uninteressant")  # Für uninteressante Bands "Uninteressant" zur Liste hinzufügen

    # Extrahieren von Datum und Wochentag aus dem Datumsfeld
    for div2 in (
            div.find_all('div', class_='field field--name-field-termin field--type-datetime field--label-hidden '
                                       'field--item')):
        # Vollständigen Datumstext ohne die letzten 8 Zeichen (Format dd.mm.yyyy) abrufen
        date_text = div2.get_text()[:-8]

        # Aufteilen des Datumstextes in Tag, Monat, Jahr
        day, month, year = date_text.split(".")

        # Tag, Monat und Jahr in Strings konvertieren
        day = str(day)
        month = str(month)
        year = str(year)

        # Erstellen eines `datetime`-Objekts aus den extrahierten Daten
        date_object = datetime.date(int(year), int(month), int(day))

        # Bestimmen der Wochentagsnummer anhand des `datetime`-Objekts
        weekday_number = date_object.weekday()

        # Extrahieren des Wochentagsnamens aus der `calendar.day_name`-Liste
        weekday = date_object.strftime("%A")[:2]  # %A für den vollständigen Wochentagsnamen

        # Übersetzen der englischen Wochentagsabkürzung ins Deutsche
        german_weekday = english_to_german_weekdays[weekday]

        # Hinzufügen der extrahierten Daten zu den entsprechenden Listen
        days.append(day)
        months.append(month)
        years.append(year)
        weekdays.append(german_weekday)

datei = open('../data/Konzertdaten.txt', 'a')

# Kombinieren der extrahierten Daten für eine kompakte Ausgabe
print("")
print("POSTHALLE WÜRZBURG:")
datei.write("POSTHALLE WÜRZBURG:\n")
for weekday, day, month, year, band in zip(weekdays, days, months, years, bands):
    if "Uninteressant" not in band:  # Filtern von "Uninteressant"-Bands
        print(f"{weekday}   {day}.{month}.{year}   {band}")
        datei.write(f"{weekday}   {day}.{month}.{year}   {band.title()}\n")

datei.write("\n")
