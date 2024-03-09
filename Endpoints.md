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

### /auth/facebook/authorized

**Wichtiger Redirect zur User Authorisierung**, über Weiterleitung über diesen Endpunkt werden User eingeloggt und einer OAuth Instanz im Backend zugeordnet

## S3

### POST /api/init_user

Für das initiale Anlegen eines Users + Organisation und evtl. Company Logo

Sample Request:

```bash
    {
        "username": "...",
        "companyname": "..."
    }
```
**UND** Logo File, wenn angegeben

Sample Response:

**200**, wenn erfolgreich User und Orga angelegt wurden (+ Files gespeichert wurden)

**400**, wenn Username/Companyname fehlt

**500**, wenn Fehler aufgetreten ist mit (zB wenn kein Ordner angelegt werden kann)
```bash
    {
        "error": "error_message"
    }
```

## S4
Company Styleguides mit File Upload

### POST /api/company_files
Request mit allen Company Files (Styleguides, Product Information etc.)

Sample Response:
**200**, wenn alle Dateien das richtige Format hatten und abgespeichert wurden
**500**, wenn Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

## S5
### GET /api/data/all_interactions
Alle Interaktionen zu einer Organisation (mit Chunks)

### GET /api/data/bookmarks
Bookmarks zu Interaktionen mit bestimmten Kunden

### GET /api/data/search_interactions
Suche nach bestimmten Interaktionen mit Filtereinstellungen

- Generate Responses zu einem Posting
- aktuellster Post
