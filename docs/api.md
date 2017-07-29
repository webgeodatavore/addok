# API

Addok expose une interface WSGI très minimaliste. Vous pouvez l'exécuter avec
 gunicorn par exemple:

    gunicorn addok.http.wsgi

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
