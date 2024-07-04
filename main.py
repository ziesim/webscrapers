import subprocess
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Laden des Verschlüsselungspassworts aus der Umgebungsvariablen
email_password = os.getenv('EMAIL_PASSWORD')

if email_password is None:
    raise ValueError("Die Umgebungsvariable 'EMAIL_PASSWORD' ist nicht gesetzt oder konnte nicht geladen werden.")

# Aktuelles Verzeichnis speichern
current_dir = os.getcwd()

# Verzeichnis setzen, in dem die Skripte ausgeführt werden sollen
os.chdir("./src/")

# Benutzer über den Beginn des Programms informieren
print("")
print("Die Ereignisse werden geladen ...")
print("Haben Sie bitte einen Moment Geduld ... ")

# schweinfurtScraper.py ausführen
subprocess.call(["python", "schweinfurtScraper.py"])

# wuerzburgScraper.py ausführen
subprocess.call(["python", "wuerzburgScraper.py"])

# wiesbadenScraper.py ausführen
subprocess.call(["python", "wiesbadenScraper.py"])

# Erfolgsmeldung nach Abschluss der Abfragen ausgeben
print("")
print("Abfrage erfolgreich!")

# E-Mail-Konfigurationsdaten
smtp_server = 'mail.gmx.net'
smtp_port = 587
email_user = 'simon_ziegler@gmx.de'

# E-Mail-Inhalt
subject = 'Konzertdaten'
recipient = 'simon_ziegler@gmx.de'

# Dateipfad
file_path = os.path.join(os.path.dirname(__file__), 'data', 'Konzertdaten.txt')

# Lese den Inhalt der Textdatei
with open(file_path, 'r') as file:
    body = file.read()

# Erstelle die E-Mail
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = recipient
msg['Subject'] = subject

# Füge den Textinhalt hinzu
msg.attach(MIMEText(body, 'plain'))

# E-Mail senden
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, recipient, msg.as_string())

print("")
print('E-Mail gesendet.')

# Arbeitsverzeichnis auf ursprüngliches Verzeichnis zurücksetzen
os.chdir(current_dir)
