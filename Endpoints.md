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

### GET /api/data/threads
Liefert Threads aller Social Media Plattformen sortiert nach Query Parametern zurück

Query Parameter
```bash
    ?sorting=YYY string (Ein Wert aus new,old,most-interaction,least-interaction)
    &offset=threadId int (ThreadID, ab dem geladen werden soll, default: 1) 
```
Der offset wird verwendet, um die ersten Interaktionen in der Sortierung anzuzeigen und nur diese zu updaten, da durch die Menge an Anfragen bei vielen Kommentaren viel Zeit vergeht. 

**200**, wenn die Anfrage erfolgreich war

Sample JSON Array mit bis zu **20** Thread Objekten:
```bash
    [
          {
              id int,
              username string,
              avatar url string,
              message string,
              platform int,
              lastUpdated datetime,
              unread bool,
              interactions int
          }
    ]
```

**204**, wenn die Anfrage erfolgreich war, aber keine Threads für diese Anfrage existieren (wenn es zB noch keine Kommentare unter Posts gibt oder in der DB noch nichts enthalten ist)

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

### POST /api/data/threads

Liefert Threads aller Social Media Plattformen gefiltert nach JSON Request zurück

JSON Post Body für Filterung / Paging:
```bash
    {
        q: string,
        platforms: int, (noch nicht implementiert, da Enums noch nicht geteilt werden)
        sentiments: [int/string] (question, positive, neutral, negative), (noch nicht implementiert)
        offset: int (id des threads nach der die weiteren threads geladen werden sollen)
    }
```

**200**, wenn die Anfrage erfolgreich war
Sample JSON Array mit bis zu **20** Thread Objekten:
```bash
    [
          {
              id int,
              username string,
              avatar url string,
              message string,
              platform int,
              lastUpdated datetime,
              unread bool,
              interactions int
          }
    ]
```

**204**, wenn die Anfrage erfolgreich war, aber keine Threads für diese Anfrage exisistieren (wenn es zB noch keine Kommentare unter Posts gibt oder die DB noch nicht aktualisiert wurde mit neuen Daten oder es keine Ergebnisse auf Grund der Filter gibt)
```bash
    []
```

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```
### GET /api/data/threads/<:threadId>

Liefert den Nachrichtenverlauf eines Threads nach threadId

**200**, wenn die Anfrage erfolgreich war
Sample JSON Array mit Message/Comment Objekten:
```bash
    [
        {
            id int (id der message/comment),
            threadId int (id des threads),
            message string,
            from int (id des users/customers),
            messageDate datetime,
        }
    ]
```

**204**, wenn die Anfrage erfolgreich war, aber keine Threads für diese Anfrage exisistieren (wenn es zB noch keine Kommentare unter Posts gibt oder die DB noch nicht aktualisiert wurde mit neuen Daten oder es keinen Thread mit der threadId gibt)
```bash
    []
```

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

### GET /api/supported_platforms

Gibt die Liste der Plattformen zurück, die aktuell implementiert sind

**200**, wenn die Anfrage erfolgreich war
Sample JSON Array mit platform Objekten:
```bash
[
    {
        "id": 1,
        "is_implemented": "1",
        "name": "Instagram"
    },
    {
        "id": 2,
        "is_implemented": "0",
        "name": "TikTok"
    },...
]
```

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

### PUT /api/data/threads/{id}

Aktualisiert einen Thread (gerade nur um den Read Status auf gelesen/ungelesen zu setzen)

JSON Post Body für Filterung / Paging:
```bash
    {
        unread bool
    }
```

**200**, wenn die Anfrage erfolgreich war ohne Response Body


**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

### POST /api/data/threads/{id}/message

Erstellt eine neue Nachricht in einem Thread

Datenstruktur im JSON Body:
```bash
    {
        message string
        [, generated_message string] (optional, wenn eine Nachricht vorher generiert wurde und diese abgeändert wurde)
    }
```


**200**, wenn die Anfrage erfolgreich war ohne Response Body

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```
### GET /api/data/bookmarks

**Nicht implementiert**

Bookmarks zu Interaktionen mit bestimmten Kunden



### GET /api/data/threads/{id}/post

**Nicht implementiert**
Liefert den zugrundeliegenden Social Media Post eines Threads

Datenstruktur der Antwort:

      {
           id int,
           threadId int,
           postMedia string (absolute url),
           postMediaType string (image, video)
           postContent string (post caption),
           platform (either id referencing the different socialmedia platforms
           in another table or string, eg. facebook),
           likes int,
           comments int,
           shares int
      }
