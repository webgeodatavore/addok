# Import de données par batch dans Addok

## Format d'import

Par défault, Addok attend un
 [stream JSON "ligne délimité"](http://en.wikipedia.org/wiki/JSON_Streaming)
 comme fichier en entrée. Cela signifie *un objet JSON par ligne*.
Optionnellement, il est possible d'utiliser msgpack. Pour cela, installez `msgpack-python` et assurez-vous que l'extension de vos fichiers de données est `.msgpack`.


#### Clés
Les clés attendues sont celles déclarées dans l'attribut `FIELDS` de votre
 [configuration](config.md), avec quelques cas spéciaux:

- **type** est attendu même s'il n'est pas déclaré comme champ d'index
- **importance** est attendu; il doit être un `float` entre 0 et 1
- **_id** est optionnel et pour un usage interne seulement, s'il n'est pas présent un [hashid](http://hashids.org/) sera généré; notez que des clés plus courtes entraine une consommation mémoire plus faible du côté de Redis
- **lat** et **lon** sont attendus
- **housenumbers** a un format spécial: `{number: {lat: yyy, lon: xxx}}`
   (optionnellement, vous pouvez ajouter n'importe quel attribut personnalisé)

Chaque valeur peut être soit une valeur unique ou une liste de valeurs.
Dans le dernier cas, la première valeur sera considérée comme celle active
(par exemple pour afficher l'étiquette), les autres, optionnelles, sont
 considérées comme des alias.
Elles seront indexées et recherchables cependant.

#### Exemple

    {"id": "091220245G","type": "street","name": "Chemin du Capitany","postcode": "09000","lat": "42.985755","lon": "1.620815","city": "Foix","departement": "Ariège", "region": "Midi-Pyrénées","importance": 0.4330 ,"housenumbers":{"13": {"lat": 42.984811,"lon": 1.620876},"15": {"lat": 42.984753,"lon": 1.620853},"39": {"lat": 42.983546,"lon": 1.621076},"8": {"lat": 42.985458,"lon": 1.621405},"23": {"lat": 42.984555,"lon": 1.620902},"29": {"lat": 42.984316,"lon": 1.620935},"37": {"lat": 42.983634,"lon": 1.621068},"19": {"lat": 42.984621,"lon": 1.620882},"33": {"lat": 42.983977,"lon": 1.621015},"6": {"lat": 42.985452,"lon": 1.621171},"25": {"lat": 42.984532,"lon": 1.620908},"21": {"lat": 42.984577,"lon": 1.620895},"1": {"lat": 42.986563,"lon": 1.620000},"11bis": {"lat": 42.985138,"lon": 1.621094},"17": {"lat": 42.984682,"lon": 1.620868},"3": {"lat": 42.986394,"lon": 1.620150}}}
    {"id": "091220259X","type": "street","name": "Avenue du Cardié","postcode": "09000","lat": "42.964308","lon": "1.595493","city": "Foix","departement": "Ariège", "region": "Midi-Pyrénées","importance": 0.4447 ,"housenumbers":{"13": {"lat": 42.964574,"lon": 1.595418},"19": {"lat": 42.964575,"lon": 1.595455},"15": {"lat": 42.964575,"lon": 1.595431},"6": {"lat": 42.964263,"lon": 1.595222},"1bis": {"lat": 42.964322,"lon": 1.596193},"17": {"lat": 42.964575,"lon": 1.595443},"23": {"lat": 42.964298,"lon": 1.594952},"27": {"lat": 42.964245,"lon": 1.594844},"1": {"lat": 42.964357,"lon": 1.596028},"2bis": {"lat": 42.964245,"lon": 1.596177},"4": {"lat": 42.964279,"lon": 1.595486},"2": {"lat": 42.964291,"lon": 1.595999},"8": {"lat": 42.964250,"lon": 1.595043},"5": {"lat": 42.964572,"lon": 1.595620},"33": {"lat": 42.963863,"lon": 1.594884},"9": {"lat": 42.964574,"lon": 1.595389},"31": {"lat": 42.964156,"lon": 1.594847},"21": {"lat": 42.964314,"lon": 1.595171},"11": {"lat": 42.964574,"lon": 1.595406},"7": {"lat": 42.964342,"lon": 1.595551},"35": {"lat": 42.963611,"lon": 1.594916},"3": {"lat": 42.964366,"lon": 1.595803},"25": {"lat": 42.964272,"lon": 1.594840}}}

#### Mise à jour et suppression

Si vous voulez gérer des diffs, vous pouvez ajouter une clé `_action` avec
 l'une des valeurs suivantes:

- `update`: va en premier désindexer le document
- `delete`: va désindexer le document; seule la clé `id` est nécessaire alors

#### Tuning de Redis

Assurez-vous d'avoir lu les [astuces de tuning de Redis](redis.md).


#### Ligne de commande
Pour exécuter l'import actuel:

    addok batch path/to/file.sjson

Ensuite, vous avez besoin d'indexer les n-grammes:

    addok ngrams

### Exemple avec BANO

1. Télécharger [la donnée BANO](http://bano.openstreetmap.fr/data/full.sjson.gz) et
   décompresser-la

2. Exécuter la commande batch:

        addok batch path/to/full.sjson

3. Indexer les segments des n-grammes:

        addok ngrams

Si vous voulez seulement un sous-ensemble de la donnée (l'ensemble du jeu de
 donnée BANO nécessite 20GB de RAM), vous pouvez l'extraire depuis un fichier complet avec une commande comme:

    sed -n 's/"Île-de-France"/&/p' path/to/full.sjson > idf.sjson

## Import depuis PostgreSQL

Voir le plugin [addok-psql](https://github.com/addok/addok-psql).


## Lire depuis stdin

La commande `import` peut lire depuis stdin, par exemple:

    $ addok batch < ~/Data/geo/ban/communes-context.json

Ou:

    $ less ~/Data/geo/ban/communes-context.json | addok batch

## Plus d'options

Exécutez `addok --help` pour voir les options disponibles.
