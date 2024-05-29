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

### POST /auth/early_access_redirect

```bash
    {
        "access_key": "...."
    }
```

Weiterleitung zu ```/login.html```, wenn access_key authentifiziert wurde, ansonsten **keine** Weiterleitung

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

Request mit allen Company Files (Styleguides, Product Information etc.) als multipart/form-data. Muss aufgerufen werden (selbst ohne files), um benötigte OpenAI Entitäten zu generieren 

**files[]**, wenn Company Files mitgesendet wurden

Sample Response:

**200**, wenn alle Dateien das richtige Format hatten und abgespeichert wurden oder es keine Dateien gab

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

### GET /api/supported_platforms

Gibt die Liste der Plattformen zurück, die aktuell implementiert sind

**200**, wenn die Anfrage erfolgreich war
Sample JSON Array mit platform Objekten:
```bash
[
    {
        "id": 1,
        "is_implemented": True,
        "name": "Instagram"
    },
    {
        "id": 2,
        "is_implemented": False,
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

### POST /api/data/threads

Liefert Threads aller Social Media Plattformen gefiltert nach JSON Request zurück, mit der aktuellsten Interaktion zuerst. Alle Query Parameter und Parameter im Post Body sind optional.

Query Parameter 
```bash
    ?sorting=YYY string (new,old,most_interaction,least_interaction)
    &offset=threadId int (ThreadID, ab dem geladen werden soll, default: 1) 
    &unread=status bool (0 oder 1)
```
Der offset wird verwendet, um die ersten Interaktionen in der Sortierung anzuzeigen und nur diese zu updaten, da durch die Menge an Anfragen bei vielen Kommentaren viel Zeit vergeht. 
Über unread kann nach allen Threads gefiltert werden, die den definierten Status haben, default werden einfach alle Threads unabhängig von ihrem Status geliefert.

JSON Post Body für Filterung / Paging:
```bash
    {
        q: string,
        platforms: int, ( ID der Plattform aus /api/supported_platforms)
        sentiments: [int/string] (question, positive, neutral, negative) (noch nicht implementiert)
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
              interactions int,
              bookmarked bool
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
### GET /api/data/threads/{id}

Liefert den Nachrichtenverlauf eines Threads nach id

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

### PUT /api/data/threads/{id}

Aktualisiert einen Thread (gerade nur um den Read Status auf gelesen/ungelesen zu setzen)

JSON Post Body:
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

### DELETE /api/data/threads/{id}

Löscht den Kommentar, zu dem der Thread erstellt wurde und den dazugehörigen Thread

**200**, wenn die Anfrage erfolgreich war ohne response body

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

### GET /api/data/threads/{id}/post

Liefert den zugrundeliegenden Social Media Post eines Threads

**200**, wenn die Anfrage erfolgreich war
Sample JSON Antwort:
```bash
    {
        "comments": 58,
        "id": 23,
        "likes": 1,
        "mediaType": "IMAGE",
        "permalink": "https://www.instagram.com/p/C3AVzmrCawb/",
        "platform": "Instagram",
        "postContent": "Heute lernen wir die Zahlen",
        "postMedia": "https://...",
        "shares": null,
        "threadId": 1,
        "timestamp": "Tue, 06 Feb 2024 12:02:42 GMT"
    }
```

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

### GET /api/data/threads/bookmarks

Liefert **20** bookmarked Threads eines Users 
Query Parameter
```bash
    ?offset=threadId int (ThreadID, ab dem geladen werden soll, default: 1) 
```

**200**, wenn die Anfrage erfolgreich war
Sample JSON Response
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
              interactions int,
              bookmarked bool
          }
    ]
```


**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

### PUT /api/data/threads/bookmarks/<threadId>

Setzt einen Thread auf den definierten Bookmarked Status

JSON Post Body:
```bash
    {
        bookmarked bool
    }
```

**200**, wenn die Anfrage erfolgreich war ohne response body

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

### POST /api/data/ai/generate_responses

Generiert Antworten zu den inhalten eines Threads

Datenstruktur im JSON Body:
```bash
    {
        threadId int
    }
```

**200**, wenn die Anfrage erfolgreich war
Sample JSON Array Antwort mit mehreren Strings:
```bash
    [
        str,
        str,
        str,
        ...
    ]
```

**400**, wenn OpenAI Probleme mit dem erstellen einer Antwort hat
```bash
    {
        "error": "error_message"
    }
```

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```

### GET /api/me

Liefert die Userinformationen zurück

**200**, wenn die Anfrage erfolgreich war
Sample JSON Antwort:
```bash
    {
        companyName str,
        name str,
        logoURL (base64 encoded data URL)
    }
```

**500**, wenn ein Fehler aufgetreten ist mit
```bash
    {
        "error": "error_message"
    }
```
