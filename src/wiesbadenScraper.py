from bs4 import BeautifulSoup  # Bibliothek zum Parsen von HTML
import requests  # Bibliothek für HTTP-Anfragen
import re  # Bibliothek für reguläre Ausdrücke
import json  # Bibliothek zum Verarbeiten von JSON-Daten

# Laden der Bandliste aus der JSON-Datei
with open('../data/Bands.json') as json_file:
    data = json.load(json_file)

# Ziel-URL definieren, von der die Konzertdaten abgerufen werden sollen
website = 'https://schlachthof-wiesbaden.de/'

# Abrufen des HTML-Inhalts der Website
result = requests.get(website)
content = result.text

# HTML-Inhalt der Webseite mit BeautifulSoup parsen
soup = BeautifulSoup(content, 'lxml')

# Den Container mit den Konzertinformationen anhand der CSS-Klasse finden
box = soup.find('div',
                class_='w-full flex flex-col items-center px-[20px] sm:px-[50px] -mt-[8px] -mt-[30px] 2xl:-mt-[35px]')

# Initialisierung der erforderlichen Listen für die extrahierten Daten
all_bands = []  # Liste für alle Bandnamen aus der JSON-Datei
weekdays = []  # Liste für Wochentage (deutsch)
days = []  # Liste für Tage (Tag)
bands = []  # Liste für Bandnamen
months = []  # Liste für Monate (Monat)
years = []  # Liste für Jahre (Jahr)

# Wörterbuch für die Umwandlung von Monatsnamen in Zahlen
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

current_month = None  # Variable zur Verfolgung des aktuellen Monats

# Alle Bandnamen aus der JSON-Datei extrahieren und in eine Liste einfügen
for band_data in data:
    band_name = band_data["bands"]
    all_bands.extend(band_name)


# Funktion zur Extraktion von Text aus einem String
def text_extrahieren(input_text):
    teile = re.split(r"/", input_text, maxsplit=1)
    if teile:
        return teile[0]
    else:
        return input_text


# Funktion zur Umwandlung eines Monatsnamens in eine Zahl
def month_to_int(monat_name):
    return complete_months.get(monat_name.title())


# Funktion zum Entfernen zusätzlicher Leerzeichen aus einem String
def remove_additional_blank(input):
    return re.sub(r'\s+', ' ', input.strip())


# Durchsuchen der HTML-Box nach Konzertinformationen
for concerts in box.find_all('div',
                             class_='w-full max-w-[800px] lg:max-w-[900px] xl:max-w-[1100px] 2xl:max-w-[1300px] '
                                    '3xl:max-w-[1500px]'):
    # Extrahieren der Wochentage der Konzerte
    for weekday in (concerts.find_all('div',
                                      class_='pt-[6px] lg:pt-[6px] xl:pt-[8px] 2xl:pt-[10px] pr-[10px] 2xl:pr-[13px] '
                                             '3xl:pr-[15px] uppercase hidden sm:inline')):
        if weekday.get_text():
            weekdays.append(remove_additional_blank(weekday.get_text()))

    # Extrahieren der Daten der Konzerte (Tag und Datum)
    for day in concerts.find_all('div',
                                 class_=(
                                         'leading-[0.88] sm:leading-[0.88] tracking-tight text-[75px] sm:text-['
                                         '100px] lg:text-[105px] xl:text-[120px] 2xl:text-[140px] 3xl:text-[150px] '
                                         'w-full font-headline uppercase',
                                         'leading-[0.88] sm:leading-[0.88] tracking-tight text-[75px] sm:text-['
                                         '100px] lg:text-[105px] xl:text-[120px] 2xl:text-[140px] 3xl:text-[150px] '
                                         'w-full font-headline uppercase -tracking-[0.08em]',
                                         'leading-[0.88] sm:leading-[0.88] tracking-tight text-[75px] sm:text-['
                                         '100px] lg:text-[105px] xl:text-[120px] 2xl:text-[140px] 3xl:text-[150px] '
                                         'w-full font-headline uppercase -tracking-[0.11em]',
                                         'leading-[0.88] sm:leading-[0.88] tracking-tight text-[75px] sm:text-['
                                         '100px] lg:text-[105px] xl:text-[120px] 2xl:text-[140px] 3xl:text-[150px] '
                                         'w-full font-headline uppercase -tracking-[0.05em]',
                                         'leading-[0.88] sm:leading-[0.88] tracking-tight text-[75px] sm:text-['
                                         '100px] lg:text-[105px] xl:text-[120px] 2xl:text-[140px] 3xl:text-[150px] '
                                         'w-full font-headline uppercase -tracking-[0.02em]')):
        if day.get_text():
            days.append(remove_additional_blank(day.get_text()))

        # Extrahieren des Monats und Jahres aus den Bildalternativtexten
        for image in (concerts.find_all('img')):
            image_alt_text = image.get("alt")

            for month in complete_months:
                if month in image_alt_text:
                    extracted_month = image_alt_text.split(" ")[0]

                    if extracted_month != current_month:
                        current_month = extracted_month

                    current_month = month_to_int(current_month)
                    current_year = image_alt_text.split(" ")[1]

                    months.append(current_month)
                    years.append(current_year)

    # Extrahieren der Bandnamen der Konzerte
    for band in (concerts.find_all('h2',
                                   class_='tracking-wider text-[25px] sm:text-[50px] xl:text-[60px] 2xl:text-[70px] '
                                          '3xl:text-[''80px] leading-[1.2] sm:leading-[1.15] 2xl:leading-[1.1] w-full '
                                          'font-headline uppercase')):
        text = remove_additional_blank(band.get_text()).lower()

        gefunden = False
        # Überprüfen, ob der Bandname in der Liste aller Bands enthalten ist
        for band_name in all_bands:
            if re.search(rf"\b{band_name}\b", text):  # Treffer am Wortanfang/Ende
                gefunden = True
                break

        # Entsprechend der Überprüfung entweder den Bandnamen hinzufügen oder "Uninteressant" einfügen
        if gefunden:
            bands.append(text_extrahieren(remove_additional_blank(band.get_text())))
        else:
            bands.append("Uninteressant")

datei = open('../data/Konzertdaten.txt', 'a')

# Ausgabe der extrahierten Daten
print("")
print("SCHLACHTHOF WIESBADEN:")
datei.write("SCHLACHTHOF WIESBADEN:\n")
for weekday, day, band, month, year in zip(weekdays, days, bands, months, years):
    if "Uninteressant" not in band:  # Konzerte filtern, die als "Uninteressant" markiert wurden
        print(f"{weekday}   {day}.{month}.{year}   {band}")
        datei.write(f"{weekday}   {day}.{month}.{year}   {band.title()}\n")

datei.write("\n")   