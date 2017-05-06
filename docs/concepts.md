# Concepts

Addok est un [géocodeur](https://fr.wikipedia.org/wiki/G%C3%A9ocodage). Il
permet de trouver des documents géographiques structurés depuis une chaîne de
caractères non structurée.


## Données

Addok accepte un chargement en batch de documents liés à une position comme
des addresses. Au minimum, la latitude et la longitude sont requises pour
chaque document indexé. Même une fois chargée, la donnée ne doit pas être
considérée comme votre référence mais comme versatile, chaque réindexation
nécessite que les fichiers source initiaux soient à nouveau chargés.

Par défaut, une base de données Redis stocke des index tandis qu'une autre
stocke des documents bruts. "Toute la donnée stockée dans Redis" signifie
qu'elle est stockée en mémoire. Vous pouvez installer un [plugin](plugins.md)
pour garder les documents dans un autre moteur de base de données (SQLite ou
PostgreSQL par exemple) pour économiser de la mémoire.


## Indexation

Chaque document est calculé à l'aide de nombreux processeurs définis dans votre
[fichier de configuration](config.md). Il y a deux étapes principales pour
gérer un document: la préparation des chaînes et le calcul des index.

Le document est découpé en tokens (par défaut des mots mais il peut s'agir de
trigrammes quand le plugin
[addok-trigrams](https://github.com/addok/addok-trigrams) est utilisé).
Chaque token deviendra un
[set ordonné Redis](https://redis.io/topics/data-types#sorted-sets) stockant
la liste des documents contenant ce token. Les filtres et les propriétés
géographiques seront aussi stockés commes des sets ordonné Redis. Une requête
de recherche consiste en des intersections de ces sets ainsi définis.


## Recherche

La recherche est un processus en trois étapes: d'abord nous nettoyons et
transformons en tokens la requête (avec les mêmes processeurs que lors de
l'indexation), ensuite nous essayons de trouver tous les candidats pour une
requête donnée et enfin nous itérerons pour ordonner les résultats par
pertinence.

Grâce à des heuristiques, nous essayons de trouver un nombre raisonnable de
candidats (environ 100) en gérant le bruit, les fautes de frappe et les
mauvaises entrées. Une fois les candidats récupérés, ils sont ordonnés
principalement par des comparaisons de chaînes.

Les importances des documents et les positions géographiques peuvent également
être prises en compte. En plus, une requête peut être filtrée explicitement
par l'émetteur en fonction des champs des documents afin de limiter le nombre
de résultats potentiels.


## L'API HTTP

Addok fournit une [API](api.md) pour interroger les données indexées via HTTP.
Il a été développé avec la performance comme une contrainte clé. Par défaut,
elle fournit des résultats sous forme de
[GeoCodeJSON](https://github.com/geocoders/geocodejson-spec/) *à plat*.

L'API a trois points d'entrée par défaut, mais vous pouvez l'étendre. L'un
consiste à effectuer une requête de recherche, le second à faire un géocodage
inverse (voir ci-dessous) et le dernier à récupérer un document.

Vous pouvez effectuer une requête de recherche avec un biais géographique,
en augmentant le poids accordé aux candidats autour d'un emplacement donné.
En outre, il permet le géocodage inverse: depuis une position à l'adresse
connue la plus proche par exemple.


## Hacking

Un binaire personnalisé lance un [interpréteur shell](shell.md) avec quelques
commandes utiles pour debugger et comprendre comment il fonctionne. Par
exemple, vous pouvez expliquez un résultat donné, montrer les résultats
d'autocomplétion pour un token donné, inspecter comment une chaîne est
transformée en tokens et ainsi de suite. Oh, et bien sûr, exécuter une
recherche!

Même si Addok se concentre sur le problème particulier des adresses - en
essayant de faire un seul travail et (nous l'espérons) en le faisant bien -
il a été développé en gardant l'extensibilité à l'esprit. Vous pouvez 
l'enrichir pour votre propre usage avec des [plugins](plugins.md) et/ou des
points d'entrée dans l'[API](api.md).

Voir aussi cette
[présentation](https://speakerdeck.com/yohanboniface/addok-presentation) pour plus de détails.
