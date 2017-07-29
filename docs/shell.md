# Commande shell Addok

Addok est fourni avec un shell intégré, qui permet d'inspecter le
 fonctionnement interne de l'index, de tester des requêtes et le traitement
 de chaîne de caractères.
Considérez-le comme un outil de debug.

Entrez dans le shell avec la commande:

    addok shell

Voici les commandes disponibles:

#### AUTOCOMPLETE
Montre les résultats de l'autocomplétion pour une chaîne donnée.

    AUTOCOMPLETE lil

#### BESTSCORE
Retourne un document lié à un mot avec le score le plus élevé.

    BESTSCORE lilas

#### BUCKET
Lance une recherche et retourne tous les résultats retournés, pas seulement ceux retournés par les éléments limités:

    BUCKET rue des Lilas

#### DBINFO
Imprime quelques infos utiles de la base de données Redis.

#### DBKEY
Imprime le contenu brut de la clé de la base de données.

    DBKEY g|u09tyzfe

#### DISTANCE
Imprime le score de distance entre deux chaînes. Utilisez | comme séparateur.

    DISTANCE rue des lilas|porte des lilas

#### EXPLAIN
Lance une recherche avec les infos de debug:

    EXPLAIN rue des Lilas

#### FREQUENCY
Retourne la fréquence d'un mot dans l'index.

    FREQUENCY lilas

#### FUZZY
Calcule les extensions floues d'un mot.

    FUZZY lilas

#### FUZZYINDEX
Calcule les extensions floues d'un mot qui existe dans l'index.

    FUZZYINDEX lilas

#### GEODISTANCE
Calcule la géodistance d'un résultat à un point.

    GEODISTANCE 772210180J 48.1234 2.9876

#### GEOHASH
Calcule un geohash depuis la latitude et la longitude.

    GEOHASH 48.1234 2.9876

#### GEOHASHMEMBERS
Retourne les membres d'un geohash et ses voisins. Utilisez "NEIGHBORS 0"
pour seulement cibler le geohash.

    GEOHASHMEMBERS u09vej04 [NEIGHBORS 0]

#### GEOHASHTOGEOJSON
Construit un GeoJSON correspondant au geohash donné comme paramètre.

    GEOHASHTOGEOJSON u09vej04

#### GET
Obtenir le document depuis l'index avec son identifiant.

    GET 772210180J

#### HELP
Afficher la liste des commandes disponibles.

#### INDEX
Obtenir les détails de l'index pour un document par son identifiant.

    INDEX 772210180J

#### INTERSECT
Faire une intersection brute entre tokens (limite par défaut à 100).

    INTERSECT rue des lilas [LIMIT 100]

#### PAIR
Voir toutes les tokens associés avec un token donné.

    PAIR lilas

#### REVERSE
Faire une recherche inverse. Arguments: lat lon.

    REVERSE 48.1234 2.9876

#### SEARCH
Lance une recherche (commande par défaut, peut être omise; les arguments entre `[]` sont optionnels):

    SEARCH rue des Lilas [CENTER lat lon] [LIMIT 10] [AUTOCOMPLETE 0]

Également, chaque filtre enregistré est disponible, par exemple:

    rue des lilas CITY hautmont

#### TOKENIZE
Inspecte comment une chaîne est tokenizée avant d'être indexée.

    TOKENIZE Rue des Lilas
