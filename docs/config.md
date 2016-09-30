# Configurer Addok

Par défaut, Addok est configuré pour une base de données adresses françaises
provenant de France
*(C'est peut être parce qu'elle a été initialement été codée à Paris… ;) )*

Mais vos besoins sont certainement différents, aussi, dans le cas, par exemple, où vous auriez à gérer des données adresses françaises, ou étrangère, vous voudrez peut-être définir **quels sont les champs à indexer** ou **quels filtres sont disponibles**.

## Enregistrement de votre fichier de configuration personnalisé

Un fichier de configuration Addok est simplement un fichier python qui
 définit quelques clés. Ce fichier peut être n'importe où dans votre système,
 et vous avez besoin de définir une variable d'environnement qui pointe
 vers
 lui:

    export ADDOK_CONFIG_MODULE=path/to/local.py

## Configurations de l'environnement

Quelques configurations sont utilisées pour définir comment addok va gérer
 le système sur lequel il est installé.

#### REDIS (dict)
Définissez les paramètres de la base de données Redis:

    REDIS = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }

#### LOG_DIR (chemin)
Chemin vers le répertoire vers lequel Addok écrira ses logs et ses fichiers
 d'historique. Il peut aussi être
 surchargé depuis la variable d'environnement `ADDOK_LOG_DIR`.

    LOG_DIR = 'path/to/dir'


## Configurations basiques

Un ensemble de Configurations que vous souhaitez peut être changer pour correspondre à votre instance personnalisée.

#### ATTRIBUTION (string ou dict)
L'attribution de la donnée qui sera utilisée dans les résultats de l'API.
Peut être une chaîne simple ou un dictionnaire Python.

    ATTRIBUTION = 'Les contributeurs OpenStreetMap'
    # Ou
    ATTRIBUTION = {source: attribution, source2: attribution2}

#### EXTRA_FIELDS (liste de dicts)
Parfois vous voulez simplement étendre les [champs par défaut](#fields-liste-de-dicts).

    EXTRA_FIELDS = [
        {'key': 'myfield'},
    ]

#### FIELDS (liste de dicts)
Les champs du document que *vous voulez indexer*. C'est une liste de dictionnaires, chacune définissant un champ indexé. Clés disponibles:

- **key** (*obligatoire*): la clé du champ dans le document
- **boost**: boost optionnel du champ, définit quelle est l'importance du champ
   dans l'index. Par exemple, un définit habituellement un boost plus importantpour le champ *name* que pour le champ *city* (par défault: 1)
- **null**: définit si le champ peut être null (par défaut: True)

```
FIELDS = [
    {'key': 'name', 'boost': 4, 'null': False},
    {'key': 'street'},
    {'key': 'postcode',
     'boost': lambda doc: 1.2 if doc.get('type') == 'commune' else 1},
    {'key': 'city'},
    {'key': 'housenumbers'}
]
```

#### FILTERS (liste)
Une liste de champs qui doivent être indexés comme des filtres disponibles.
Souvenez-vous que chaque filtre signifie un index plus gros.

    FILTERS = ["type", "postcode"]

#### HOUSENUMBERS_PAYLOAD_FIELDS (liste de clés)
Si vous souhaitez stocker des champs supplémentaires avec chaque 'payload'.
Ces champs ne seront pas recherchables, mais seront retournés dans le résultat
 de la recherche.

    HOUSENUMBERS_PAYLOAD_FIELDS = ['key1', 'key2']

#### LICENCE (string ou dict)
La licence de la donnée retournée dans les résultats de l'API.
Elle peut être une chaîne simple ou un dictionnaire Python.

    LICENCE = "ODbL"
    # Ou
    LICENCE = {source: licence, source2: licence2}

#### LOG_QUERIES (booléen)
Mettez-le à `True` pour avoir les logs de chaque requête reçue et chaque
 premier résultat si présent. *Note: seules les requêtes sont logguées, aucune
 des autres données reçues.*

    LOG_QUERIES = False

#### LOG_NOT_FOUND (booléen)
Mettez-le à `True` pour avoir les logs de chaque requête non trouvée via le
 point d'entrée `search` ou celui `csv`.

    LOG_NOT_FOUND = False

#### HOUSENUMBER_PROCESSORS (itérable de chemins python)
Traitements additionnels qui sont exécutés seulement pour les noms de maison.

    HOUSENUMBER_PROCESSORS = [
        'addok.textutils.fr_FR.glue_ordinal',
    ]

#### PROCESSORS (itérable de chemins python)
Définit les différentes fonctions pour prétraiter le texte, avant l'indexation et la recherche. C'est un `itérable` de chemins python. Quelques fonctions sont incluses
(principalement pour le français pour le moment, mais vous pouvez pointer vers n'importe quelle fonction qui est dans le pythonpath).

    PROCESSORS = [
        'addok.textutils.default.pipeline.tokenize',
        'addok.textutils.default.pipeline.normalize',
        'addok.textutils.default.pipeline.synonymize',
        'addok.textutils.fr.phonemicize',
    ]

#### QUERY_PROCESSORS (itérable de chemins python)
Traitements additionnels qui sont exécutés seulement au moment de la requête.

    QUERY_PROCESSORS = (
        'addok.textutils.fr_FR.extract_address',
        'addok.textutils.fr_FR.clean_query',
        'addok.textutils.fr_FR.glue_ordinal',
    )

#### SYNONYMS_PATH (chemin)
Chemin vers le fichier de synonymes. Le fichier de synonymes est dans le format `av, ave => avenue`.

    SYNONYMS_PATH = RESOURCES_ROOT.joinpath('synonyms').joinpath('fr.txt')

## Configurations avancées

Il s'agit des configurations internes. Changez-les avec précaution.

#### BUCKET_LIMIT (int)
Le nombre maximal d'élements qu'addok essayera de récupérer depuis Redis avant
 le scoring et de les trier. Notez que **cela n'est pas le nombre de résultats
 retournés**.

    BUCKET_LIMIT = 1000

#### COMMON_THRESHOLD (int)
Au-dessus de ce seuil, les termes sont considérés comme habituels, et ainsi
 avec moins d'importance dans l'algorithme de recherche.

    COMMON_THRESHOLD = 10000

#### DEFAULT_BOOST (float)
Score par défaut pour le token de relation avec le document.

    DEFAULT_BOOST = 1.0

#### GEOHASH_PRECISION (int)
Taille du geohash. Le plus important est la valeur, la plus petite est le hash.
Voir [Geohash sur Wikipedia (en)](http://en.wikipedia.org/wiki/Geohash).

    GEOHASH_PRECISION = 8

#### IMPORTANCE_WEIGHT (float)
Le score max inhérent d'un document dans le score final.

    IMPORTANCE_WEIGHT = 0.1

#### INTERSECT_LIMIT (int)
Au dessus de ce seuil, nous évitons d'intersecter des 'sets'.

    INTERSECT_LIMIT = 100000

#### MAX_EDGE_NGRAMS (int)
Longueur maximum d'un segment n-grammes calculé.

    MAX_EDGE_NGRAMS = 20

#### MIN_EDGE_NGRAMS (int)
Longueur minimum d'un segment n-grammes calculé.

    MIN_EDGE_NGRAMS = 3

#### MAKE_LABELS (func)
Fonction qui surcharge les étiquettes construites pour la comparaison de chaînes avec la requête au moment du scoring. Elle accepte un objet `result` comme argument et doit retourner une liste de chaînes de caractère.

    MAKE_LABELS = lambda r: return [r.name + 'my custom thing']

#### MATCH_THRESHOLD (float entre 0 et 1)
Score minimum utilisé pour considérer qu'un résultat puisse *correspondre* à la requête.

    MATCH_THRESHOLD = 0.9

## Paramètres PostgreSQL

Addok peut requêter n'importe quelle base de données PostgreSQL. Par défaut,
 il est configuré pour interroger une base de données Nominatim.

#### PSQL (dict)
Paramètres d'authentification pour se connecter à la base de données
 PostgreSQL. Utilisée pour importer les données depuis Nominatim par exemple.

    PSQL = {
        'dbname': 'nominatim'
    }

#### PSQL_EXTRAWHERE (string)
Ajout optionnel d'une clause 'where' à la requête par défaut.

    PSQL_EXTRAWHERE = ''

#### PSQL_ITERSIZE (int)
Taille du curseur de connexion.

    PSQL_ITERSIZE = 1000

#### PSQL_LIMIT (int)
Limite optionnelle quand on requête PostgreSQL.

    PSQL_LIMIT = None

#### PSQL_PROCESSORS (iterable)
Itérable de modules pour prétraiter les données PostgreSQL.

    PSQL_PROCESSORS = (
        'addok.batch.psql.query',
        'addok.batch.nominatim.get_context',
        'addok.batch.nominatim.get_housenumbers',
        'addok.batch.nominatim.row_to_doc',
    )

#### PSQL_QUERY (string)
Requête par défault exécutée quand une importation est faite depuis PostgreSQL.

    PSQL_QUERY = 'SELECT …'
