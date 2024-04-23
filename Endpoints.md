# Endpoints

## "Coming Soon" Page
### POST /auth/early_access
Sample Request:

```bash
    {
        "access_key": "...."
    }
```

Sample Response:

**200**, wenn der Key authentifiziert werden kann

**400**, wenn kein Key gegeben wurde

**403**, wenn der Key nicht authentifiziert werden kann


## S1
Meta Auth Redirect für Login

### /auth/facebook

**Wichtiger Redirect zur User Authorisierung**, über Weiterleitung über diesen Endpunkt werden User eingeloggt und einer OAuth Instanz im Backend zugeordnet

## S3

### POST /api/init_user

Für das initiale Anlegen eines Users + Organisation und evtl. Company Logo

Sample Request als multipart/form-data:

```bash
username: ...
companyname: ...
```
**Optional** *file*, wenn ein Logo File hochgeladen wurde

Sample Response:

**200**, wenn erfolgreich User und Orga angelegt wurden (+ Files gespeichert wurden)

**400**, wenn Username/Companyname fehlt

**500**, wenn Fehler aufgetreten ist (zB wenn kein Ordner angelegt werden kann)
```bash
    {
        "error": "error_message"
    }
```

## S4
Company Styleguides mit File Upload

### POST /api/company_files

Request mit allen Company Files (Styleguides, Product Information etc.) als multipart/form-data

**files[]**, wenn Company Files mitgesendet wurden

Sample Response:

**200**, wenn alle Dateien das richtige Format hatten und abgespeichert wurden

**422**, wenn mindestens ein Fehler aufgetreten ist bei der Verarbeitung der Dateien mit
```bash
    {
        "error": ["error_message", "error_message", "..."],
        "successful": "filename1, filename2, ..."
    }
```

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

## S5
### GET /api/data/all_interactions

**Nicht implementiert**

Alle Interaktionen zu einer Organisation (mit Chunks)

### GET /api/data/bookmarks

**Nicht implementiert**

Bookmarks zu Interaktionen mit bestimmten Kunden

### GET /api/data/search_interactions

**Nicht implementiert**

Suche nach bestimmten Interaktionen mit Filtereinstellungen

- Generate Responses zu einem Posting
- aktuellster Post

### POST /api/data/threads[/{sorting}]

Liefert Threads aller Social Media Plattform zurück

Struktur der Anfrage:
GET Parameter für Sortierung (entweder new, old, most-interaction oder
least-interaction)

JSON Post Body für Filterung:

     {
          platforms: [int/string],
          sentiments: [int/string] (question, positive, neutral, negative),
     }

platforms kann entweder die Namen der Social Media Plattformen als Array aus String oder -
falls du intern eine Mapping Tabelle hast - als referenzierende Id

sentiments wie bei platforms, entweder als Array aus String oder als int

Struktur der Antwort:
JSON Array mit Thread Objekten:

     [
          {
              id int,
              username string,
              message string,
              platform int/string,
              lastUpdated datetime,
              unread bool,
          }
     ]
