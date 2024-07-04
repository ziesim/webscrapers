# Konzert-Scraping mit Python

Dieses Projekt ermöglicht das automatisierte Scrapen von Konzertinformationen von verschiedenen Veranstaltungswebsites mithilfe von Python. Es nutzt Web-Scraping-Techniken, um Informationen wie Bandnamen, Veranstaltungsdaten und -orte von ausgewählten Websites zu extrahieren.

### Verwendete Bibliotheken

- **selenium:** Eine Python-Bibliothek zur Automatisierung von Webbrowser-Interaktionen, die für das dynamische Laden von Inhalten und das Klicken auf Elemente auf Webseiten verwendet wird.
- **requests:** Eine einfache HTTP-Bibliothek für Python, die für das Senden von HTTP-Anfragen und das Empfangen von HTTP-Antworten verwendet wird, insbesondere für den initialen Zugriff auf Webseiten.
- **bs4 (Beautiful Soup):** Eine Bibliothek zur Extraktion von Daten aus HTML- und XML-Dokumenten. Sie wird verwendet, um spezifische Elemente aus dem Quellcode der Webseiten zu finden und zu extrahieren.
- **lxml:** Eine leistungsstarke Bibliothek für die Verarbeitung von XML und HTML in Python, die für das Parsen und Navigieren durch HTML-Dokumente verwendet wird.
- **flake8:** Ein Werkzeug zur statischen Codeanalyse, das für die Überprüfung und Einhaltung des Python-Code-Stils gemäß den *PEP-8-Richtlinien* verwendet wird.

### Ausführung des Scrapers

Der Hauptcode besteht aus mehreren Python-Skripten (*schweinfurtScraper.py, wuerzburgScraper.py, wiesbadenScraper.py*), die jeweils für spezifische Websites konfiguriert sind. Diese Skripte werden nacheinander ausgeführt, um Konzertinformationen von den entsprechenden Websites zu sammeln.

```bash
python main.py
```

Die Datei *main.py* koordiniert den Aufruf der einzelnen Skripte für jede Stadt.

### Ergebnisse
Nach dem Ausführen der Skripte werden die extrahierten Konzertinformationen auf der Konsole ausgegeben. Das Ergebnis umfasst Wochentag, Datum und Bandname.

### Hinweise

-   **Web-Scraping Ethik:** Beim Web-Scraping ist es wichtig, die ethischen Richtlinien der jeweiligen Websites zu respektieren. Überprüfen Sie die Nutzungsbedingungen der Websites und stellen Sie sicher, dass Sie keine rechtlichen Bestimmungen verletzen.
-   **Anpassung:** Die Skripte können je nach den spezifischen Anforderungen und der Struktur der Websites angepasst werden. Beachten Sie Änderungen in der HTML-Struktur und passen Sie die Selektoren entsprechend an.
-   **Automatisierung:** Das Projekt kann durch Zeitpläne und automatisierte Ausführung erweitert werden, um regelmäßig Konzertinformationen zu aktualisieren und zu überwachen.

### Autoren

Dieses Projekt wurde von Simon Ziegler entwickelt. Kontaktieren Sie mich gerne bei Fragen oder Feedback.

### Lizenz

Dieses Projekt ist unter der **MIT-Lizenz** lizenziert. Sie können den Code frei verwenden, kopieren und ändern.
