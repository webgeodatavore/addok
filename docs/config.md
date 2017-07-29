# Configurer Addok

Par défaut, Addok est configuré pour une base de données adresses françaises
provenant de France
*(C'est peut être parce qu'elle a été initialement été codée à Paris… ;) )*

Mais vos besoins sont certainement différents, et même si vous avez des 
adresses françaises, vous voudrez peut-être définir **quels sont les champs à
 indexer** ou **quels filtres sont disponibles** par exemple.

*Voir aussi le [tuning de Redis](redis.md).*

## Enregistrement de votre fichier de configuration personnalisé

Un fichier de configuration Addok est simplement un fichier Python qui
 définit quelques clés. Son emplacement par défaut est `/etc/addok/addok.conf`.
Mais peut être n'importe où dans votre système, et vous avez besoin de définir
 une variable d'environnement qui pointe vers lui si vous voulez un emplacement
 particulier:

    export ADDOK_CONFIG_MODULE=path/to/local.py

Vous pouvez aussi utilisez l'argument `--config` quand vous lancer la ligne de
 commande `addok`.

Le fichier de configuration par défaut est dans `addok/config/default.py`.

## Configurations de l'environnement

Quelques paramètres sont utilisés pour définir comment addok va gérer
 le système sur lequel il est installé.

#### REDIS (dict)
Définissez les paramètres de la base de données Redis:

    REDIS = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }

Par défaut, en utilisant `RedisStore` pour les documents, les index et les
 documents seront stockés dans deux bases de données Redis.
Vous pouvez contrôler ces détails en utilisant les sous-dictionnaires
 `indexes` et/ou `documents`, par exemple:

    REDIS = {
        'host': 'myhost',
        'port': 6379,
        'indexes': {
            'db': 11,
        },
        'documents': {
            'db': 12,
        }
    }

Si vos hôtes sont différents, vous pouvez les définir comme ceci:

    REDIS = {
        'port': 6379,
        'indexes': {
            'host': 'myhost1',
            'db': 11,
        },
        'documents': {
            'db': 12,
            'host': 'myhost2',
        }
    }

et bien sûr, il en est de même pour le port.


#### LOG_DIR (chemin)
Chemin vers le répertoire vers lequel Addok écrira ses logs et ses fichiers
 d'historique. Il peut aussi être surchargé depuis la variable
 d'environnement `ADDOK_LOG_DIR`.

    LOG_DIR = 'path/to/dir'

Ce paramètre prend comme valeur par défaut le répertoire racine du package
 addok.

## Configurations basiques

Un ensemble de paramètres que vous souhaitez peut être changer pour
 correspondre à votre instance personnalisée.

Attention: vous verrez de nombreux paramètres suffixés avec PYPATH(S), ceux-ci
 attendent des chemins vers des callable Python. Dans le cas d'une liste,
l'ordre compte étant donné qu'il s'agit d'une chaîne de traitements.

#### ATTRIBUTION (string ou dict)
L'attribution de la donnée qui sera utilisée dans les résultats de l'API.
Peut être une chaîne simple ou un dictionnaire Python.

    ATTRIBUTION = 'Les contributeurs OpenStreetMap'
    # Ou
    ATTRIBUTION = {'source': 'attribution', 'source2': 'attribution2'}

#### BATCH_WORKERS (int)
Nombre de processus en utilisation quand sont parallélisées des tâches comme
 des imports par batch ou le calcul des ngrams.

    BATCH_WORKERS = os.cpu_count() - 1

#### DOCUMENT_STORE_PYPATH (chemin Python)
Chemin Python vers une classe de stockage pour sauver les documents utilisant
 un autre moteur et sauver de la mémoire.
Allez voir la documentation dédiée dans la page sur les [plugins](plugins.md).

#### EXTRA_FIELDS (liste de dicts)
Parfois vous voulez simplement étendre les [champs par défaut](#fields-liste-de-dicts).

    EXTRA_FIELDS = [
        {'key': 'myfield'},
    ]

#### FIELDS (liste de dicts)
Les champs du document que *vous voulez indexer*. C'est une liste de
 dictionnaires, chacune définissant un champ indexé. Clés disponibles:

- **key** (*obligatoire*): la clé du champ dans le document
- **boost**: boost optionnel du champ, définit quelle est l'importance du champ
   dans l'index. Par exemple, un définit habituellement un boost plus important pour le champ *name* que pour le champ *city* (par défault: 1)
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

#### LICENCE (string ou dict)
La licence de la donnée retournée dans les résultats de l'API.
Elle peut être une chaîne simple ou un dictionnaire Python.

    LICENCE = "ODbL"
    # Ou
    LICENCE = {'source': 'licence', 'source2': 'licence2'}

#### LOG_QUERIES (booléen)
Mettez-le à `True` pour avoir les logs de chaque requête reçue et chaque
 premier résultat si présent. *Note: seules les requêtes sont logguées, aucune
 des autres données reçues.*

    LOG_QUERIES = False

#### LOG_NOT_FOUND (booléen)
Mettez-le à `True` pour avoir les logs de chaque requête non trouvée via le
 point d'entrée `search` ou celui `csv`.

    LOG_NOT_FOUND = False

#### QUERY_MAX_LENGTH (int)
En caractères, longueur maximum acceptée de la requête. Évite de traiter des
 chaînes très longues.

    QUERY_MAX_LENGTH = 200

#### SYNONYMS_PATH (chemin)
Chemin vers le fichier de synonymes. Le fichier de synonymes est dans le
 format `av, ave => avenue`.

    SYNONYMS_PATH = '/path/to/synonyms.txt'

## Configurations avancées

Il s'agit des configurations internes. Changez-les avec précaution.

#### BATCH_CHUNK_SIZE (int)
Nombre de documents devant être traité en même temps par chaque worker pendant
 l'import.

    BATCH_CHUNK_SIZE = 1000

#### BATCH_FILE_LOADER_PYPATH (chemin Python)
Chemin Python vers un callable qui sera responsable du chargement du fichier
 d'import et retournera un itérable.

    BATCH_FILE_LOADER_PYPATH = 'addok.helpers.load_file'

#### BATCH_PROCESSORS_PYPATHS (itérable de chemins Python)
Toutes les méthodes appelées pendant le processus de batch.

    BATCH_PROCESSORS_PYPATHS = [
        'addok.batch.to_json',
        'addok.helpers.index.prepare_housenumbers',
        'addok.ds.store_documents',
        'addok.helpers.index.index_documents',
    ]

#### BUCKET_MIN (int)
Le nombre minimal d'élements qu'addok essayera de récupérer depuis Redis avant
 le scoring et de les trier. Notez que **cela n'est pas le nombre de résultats
 retournés**. Cela peut impacter fortement les performances.

    BUCKET_MIN = 10

#### BUCKET_MAX (int)
Le nombre maximal d'élements qu'addok essayera de récupérer depuis Redis avant
 le scoring et de les trier. Notez que **cela n'est pas le nombre de résultats
 retournés**. Cela peut impacter fortement les performances.

    BUCKET_MAX = 100

#### COMMON_THRESHOLD (int)
Au-dessus de ce seuil, les termes sont considérés comme habituels, et ainsi
 avec moins d'importance dans l'algorithme de recherche.

    COMMON_THRESHOLD = 10000

#### DEFAULT_BOOST (float)
Score par défaut pour le token de relation avec le document.

    DEFAULT_BOOST = 1.0

#### DOCUMENT_SERIALIZER_PYPATH (chemin Python)
Chemin vers le sérialiseur à utiliser pour stocker les documents. Il doit
 avoir les méthodes `loads` et `dumps`.

    DOCUMENT_SERIALIZER_PYPATH = 'addok.helpers.serializers.ZlibSerializer'

Pour une option plus rapide (mais utilisant plus de de RAM), utilisez `marshal`
 à la place.

    DOCUMENT_SERIALIZER_PYPATH = 'marshal'

#### GEOHASH_PRECISION (int)
Taille du geohash. Plus la valeur est importante et plus le hash est petit.
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

#### MIN_EDGE_NGRAMS (entier)
Longueur minimum d'un segment n-grammes calculé.

    MIN_EDGE_NGRAMS = 3

#### MIN_SCORE (flottant)
Tous les résultats avec un score final en dessous de ce seuil ne seront pas
 gardés. Le score est entre 0 et 1.

    MIN_SCORE = 0.1

#### MAKE_LABELS (func)
Fonction qui surcharge les étiquettes construites pour la comparaison de
 chaînes avec la requête au moment du scoring. Elle accepte un objet
 `result` comme argument et doit retourner une liste de chaînes de caractère.

    MAKE_LABELS = lambda r: return [r.name + 'my custom thing']

#### MATCH_THRESHOLD (float entre 0 et 1)
Score minimum utilisé pour considérer qu'un résultat puisse *correspondre* à la requête.

    MATCH_THRESHOLD = 0.9

#### PROCESSORS_PYPATHS (itérable de chemins Python)
Définit les différentes fonctions pour prétraiter le texte, avant l'indexation
 et la recherche. C'est un `itérable` de chemins Python. Quelques fonctions
 sont incluses (principalement pour le français pour le moment, mais vous
 pouvez pointer vers n'importe quelle fonction qui est dans le pythonpath).

    PROCESSORS_PYPATHS = [
        'addok.helpers.text.tokenize',
        'addok.helpers.text.normalize',
        'addok.helpers.text.flag_housenumber',
        'addok.helpers.text.synonymize',
    ]

#### QUERY_PROCESSORS_PYPATHS (itérable de chemins Python)
Traitements additionnels qui sont exécutés seulement au moment de la requête.
Par défaut, seulement `check_query_length` est actif, il dépend de `QUERY_MAX_LENGTH` pour éviter un DoS.

    QUERY_PROCESSORS_PYPATHS = (
        'addok.helpers.text.check_query_length',
    )

#### RESULTS_COLLECTORS_PYPATHS (itérable de chemins Python)
Addok essayera chacune de ces fonctions dans l'ordre donné pour chercher les résultats qui correspondent.

    RESULTS_COLLECTORS_PYPATHS = [
        'addok.helpers.collectors.no_tokens_but_housenumbers_and_geohash',
        'addok.helpers.collectors.no_available_tokens_abort',
        'addok.helpers.collectors.only_commons',
        'addok.helpers.collectors.bucket_with_meaningful',
        'addok.helpers.collectors.reduce_with_other_commons',
        'addok.helpers.collectors.ensure_geohash_results_are_included_if_center_is_given',
        'addok.helpers.collectors.extend_results_reducing_tokens',
        'addok.helpers.collectors.extend_results_extrapoling_relations',
    ]

### SEARCH_RESULT_PROCESSORS_PYPATHS (itérable de chemins Python)
Traitement postérieur de chaque résultat trouvé pendant la recherche.

    SEARCH_RESULT_PROCESSORS_PYPATHS = [
        'addok.helpers.results.match_housenumber',
        'addok.helpers.results.make_labels',
        'addok.helpers.results.score_by_importance',
        'addok.helpers.results.score_by_autocomplete_distance',
        'addok.helpers.results.score_by_ngram_distance',
        'addok.helpers.results.score_by_geo_distance',
    ]
