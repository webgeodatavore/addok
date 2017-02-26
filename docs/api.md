# API

Addok expose une interface WSGI très minimaliste. Vous pouvez l'exécuter avec
 gunicorn par exemple:

    gunicorn addok.server:app

Pour le debug, vous pouvez exécuter le serveur Werkzeug simple:

    addok serve

## Points d'entrée

### /search/

Retourne une recherche plein texte.

#### Paramètres

- **q** *(requis)*: chaîne à rechercher
- **limit**: limiter le nombre de résultats (par défaut: 5)
- **autocomplete**: activer ou désactiver l'autocompletion (par défault: 1)
- **lat**/**lon**: définir un centre pour donner une priorité aux résultats
  proche de de ce centre (**lng** est aussi accepté à la place de **lon**)
- chaque filtre qui a été déclaré dans la [configuration](config.md) est
  disponible en tant que paramètre

#### Format de la réponse

Le format de la réponse suit la [spécification GeoCodeJSON](https://github.com/geocoders/geocodejson-spec).
Voici un exemple:

```
{
    "attribution": "BANO",
    "licence": "ODbL",
    "query": "8 bd du port",
    "type": "FeatureCollection",
    "version": "draft",
    "features": [
        {
            "properties":
            {
                "context": "80, Somme, Picardie",
                "housenumber": "8",
                "label": "8 Boulevard du Port 80000 Amiens",
                "postcode": "80000",
                "id": "800216590L",
                "score": 0.3351181818181818,
                "name": "8 Boulevard du Port",
                "city": "Amiens",
                "type": "housenumber"
            },
            "geometry":
            {
                "type": "Point",
                "coordinates": [2.29009, 49.897446]
            },
            "type": "Feature"
        },
        {
            "properties":
            {
                "context": "34, H\u00e9rault, Languedoc-Roussillon",
                "housenumber": "8",
                "label": "8 Boulevard du Port 34140 M\u00e8ze",
                "postcode": "34140",
                "id": "341570770U",
                "score": 0.3287575757575757,
                "name": "8 Boulevard du Port",
                "city": "M\u00e8ze",
                "type": "housenumber"
            },
            "geometry":
            {
                "type": "Point",
                "coordinates": [3.605875, 43.425232]
            },
            "type": "Feature"
        }
    ]
}
```

### /reverse/

Retourne un géocodage inverse.

Paramètres:

- **lat**/**lon**: centre pour faire un géocodage inverse (**lng** est aussi
  accepté à la place de **lon**)
- chaque filtre qui a été déclaré dans la [configuration](config.md) est
  disponible en tant que paramètre

Le format de réponse est le même que pour le point d'entrée `/search/`.


### /search/csv/

Géocode sous forme batch un fichier csv.

#### Paramètres

- **data**: fichier csv qui doit être traité
- **columns**: définit les colonnes du csv qui doivent être concaténées pour
   créer la chaîne de recherche (une colonne par paramètre `columns`; par
   défaut: toutes les colonnes du fichier sont utilisées)
- **encoding** (optionnel): encodage du fichier (vous pouvez aussi spécifier
   un jeu de caractères `charset` dans le mimetype du fichier), comme 'utf-8'
   ou 'iso-8859-1'
- **delimiter** (optionnel): délimiteur CSV
- chaque filtre qui a été déclaré dans la [configuration](config.md) est
   disponible en tant que paramètre, et vous devez renseigner le nom de la
   colonne à utiliser comme valeur; par exemple, si vous voulez filtrer par
   'postcode' et que vous avez une colonne 'code postal' contenant un code
   postal de chaque ligne, vous passerez `postcode=code postal` et chaque
   ligne sera filtrée selon la valeur de la colonne 'code postal'
- les paramètres `lat` et `lon`, comme les filtres, peuvent être utilisés pour
   définir les noms de colonnes qui contiennent les valeurs de latitude et
   longitude, pour ajouter un centre de préférence pour géocoder chaque ligne

#### Exemples

    http -f POST http://localhost:7878/search/csv/ columns='voie' columns='ville' data@path/to/file.csv
    http -f POST http://localhost:7878/search/csv/ columns='rue' postcode='code postal' data@path/to/file.csv

### /reverse/csv/

Fait un géocodage inverse par batch d'un fichier csv.

#### Paramètres

- **data**: fichier csv qui doit être traité; il doit contenir les colonnes
   `latitude` (ou `lat`) et `longitude` (ou `lon` ou `lng`)
- **encoding** (optionnel): encodage du fichier (vous pouvez aussi spécifier
   un jeu de caractères `charset` dans le mimetype du fichier), comme 'utf-8'
   ou 'iso-8859-1'
- **delimiter** (optionnel): délimiteur CSV
- chaque filtre qui a été déclaré dans la [configuration](config.md) est
   disponible en tant que paramètre, et vous devez renseigner le nom de la
   colonne à utiliser comme valeur; par exemple, si vous voulez filtrer par
   'postcode' et que vous avez une colonne 'code postal' contenant un code
   postal de chaque ligne, vous passerez `postcode=code postal` et chaque
   ligne sera filtrée selon la valeur de la colonne 'code postal'

### /get/&lt;doc_id&gt;/

Récupére un document depuis son identifiant.

#### Paramètres

- **doc_id**: l'identifiant du document
