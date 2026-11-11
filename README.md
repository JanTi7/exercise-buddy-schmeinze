# Übungs-Buddy

Proof-of-Concept: Übungen für zu Hause anhaken und als A4-Blatt ausdrucken – statt sie jedem Patienten von Hand aufzuschreiben.

## Benutzen

1. `UebungsBuddy.exe` herunterladen und doppelklicken (64-Bit-Windows 10/11, keine Installation).
2. Die Oberfläche öffnet sich im Browser. Links Übungen anhaken, rechts erscheint die Vorschau.
3. **Drucken** klicken. Drei Übungen passen auf eine Seite.

Das kleine schwarze Fenster ist das Programm selbst – schließen beendet es.
Beim ersten Start warnt Windows eventuell (SmartScreen): „Weitere Informationen“ → „Trotzdem ausführen“.

## Übungen pflegen

- **+ Neue Übung**: Name, Kategorie, Stichpunkte (eine Zeile = ein Punkt), Bilder.
- **✎** neben einer Übung: bearbeiten oder löschen.
- **Praxis / Logo**: Kopfzeile des Blatts.

Alles wird in `uebungen.json` neben der exe gespeichert. Diese Datei ist der Datenpool: mitkopieren = Backup bzw. Umzug auf einen anderen Rechner. Fehlt sie, startet das Programm mit den eingebauten Beispielübungen.

Die mitgelieferten Übungstexte sind Platzhalter und nicht fachlich geprüft.

## Entwickeln

Ein kleiner Go-Webserver (`main.go`) liefert die Oberfläche (`index.html`) auf `127.0.0.1:47811` aus und liest/schreibt die JSON-Datei.

```sh
GOOS=windows GOARCH=amd64 go build -ldflags "-s -w" -o UebungsBuddy.exe .
```

`python3 gen_seed.py` erzeugt die Beispielübungen samt Strichmännchen neu (`seed.json`, wird in die exe eingebettet).
