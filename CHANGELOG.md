## 1.0.0

- changement cassant: la clé "id" n'est plus requise dans la donnée chargée
   et en tant que tel a été retirée de la racine la Feature GeoJSON.

## 1.0.0-rc.4

- housenumbers are not indexed anymore (to gain RAM), they are only matched in
  result postprocessing
- for `addok-france` users: `addok_france.match_housenumber` should be replaced
  by `addok.helpers.results.match_housenumber` in SEARCH_RESULT_PROCESSORS_PYPATHS
- new `MIN_SCORE` setting to filter out results with very low scores
- for `addok-france` users: fixed leading zeros wrongly removed from postcodes

## 1.0.0-rc.3

- suppression de `DOCUMENT_PROCESSORS_PYPATHS` en faveur de `BATCH_PROCESSORS_PYPATHS`
  (pas utilisé avant la 1.0.0-rc.1)
- ajout de `BATCH_FILE_LOADER_PYPATH` pour spécifier un fichier personnalisé
   de chargement (comme msgpack)

## 1.0.0-rc.1

La 1.0.0 a été une grosse réécriture, avec comme fonctionnalités principales:

- découpage en [plugins](http://addok.readthedocs.io/en/latest/plugins/)
- possibilité de stockage externe de documents (dans SQLite, PostgreSQL, etc.)
- utilisation du scripting de LUA pour les performances
- moins de consommation de RAM
- remplacement de Flask par Falcon pour les performances
- les housenumbers ne sont plus indexées (pour gagner de la RAM), elles sont
   seulement vérifiées dans le post-traitement du résultat

Elle contient de nombreux changements "cassants". La meilleure des options
quand c'est possible est de redémarrer depuis le début (voir le
[tutoriel](http://addok.readthedocs.io/en/latest/tutorial/)) et de réindexer
tout.

### Changements "cassants"

- `PROCESSORS`, `INDEXERS`, etc. ont été renommés en `PROCESSORS_PYPATHS`,
  `INDEXERS_PYPATHS`, etc.
- `HOUSENUMBERS_PROCESSORS` a été supprimé
- config doit maintenant être chargé avec `from addok.config import config`
- suppression de `DEINDEXERS`, maintenant `INDEXERS` doit pointer vers des
  classes Python ayant les deux méthodes `index` and `deindex`
- changements des points d'entrée de l'API
- par défaut, les documents sont maintenant stockés dans une base de données Redis séparée


### Changements mineurs

- indexation de multiples valeurs dans les filtres
- ajout d'une commande "reset" pour réinitialiser toutes les données(index et
  documents)
- ajout du paramètre `quote` pour les points d'entrée CSV (maintenant dans
  le plugin addok-csv)
- addok essaye maintenant de lire la configuration depuis
  `/etc/addok/addok.conf` comme solution de repli
- `SMALL_BUCKET_LIMIT` est maintenant un paramètre

Allez aussi voir la nouvelle section
[FAQ](http://addok.readthedocs.io/en/latest/faq/) dans la documentation.


## 0.5.0
- Expose housenumber parent name in result geojson
- add support for housenumber payload ([#134](https://github.com/etalab/addok/issues/134))
- Fix clean_query being too much greedy for "cs" ([#125](https://github.com/etalab/addok/issues/125)
- also accept long for longitude
- replace "s/s" in French preprocessing
- fix autocomplete querystring casting to boolean
- Always add housenumber in label candidates if set ([#120](https://github.com/etalab/addok/issues/120))
- make CSVView more hackable by plugins ([#116][https://github.com/etalab/addok/issues/116))


## 0.4.0
- fix filters not taken into account in manual scan ([#105](https://github.com/etalab/addok/issues/105))
- added experimental list support for document values
- Added MIN_EDGE_NGRAMS and MAX_EDGE_NGRAMS settings ([#102](https://github.com/etalab/addok/issues/102))
- documented MAKE_LABELS setting
- Allow to pass functions as PROCESSORS, instead of path
- remove raw housenumbers returned in result properties
- do not consider filter if column is empty, in csv ([#109](https://github.com/etalab/addok/issues/109))
- allow to pass lat and lon to define columns to be used for geo preference, in csv ([#110](https://github.com/etalab/addok/issues/110))
- replace "s/" by "sur" in French preprocessing ([#107](https://github.com/etalab/addok/issues/107))
- fix server failing when document was missing `importance` value
- refuse to load if `ADDOK_CONFIG_MODULE` is given but not found
- allow to set ADDOK_CONFIG_MODULE with command line parameter `--config`
- mention request parameters in geojson ([#113](https://github.com/etalab/addok/issues/113))


## 0.3.1

- fix single character wrongly glued to housenumber ([#99](https://github.com/etalab/addok/issues/99))

## 0.3.0

- use housenumber id as result id, when given ([#38](https://github.com/etalab/addok/issues/38))
- shell: warn when requested id does not exist ([#75](https://github.com/etalab/addok/issues/75))
- print filters in debug mode
- added filters to CSV endpoint ([#67](https://github.com/etalab/addok/issues/67))
- also accept `lng` as parameter ([#88](https://github.com/etalab/addok/issues/88))
- add `/get/` endpoint ([#87](https://github.com/etalab/addok/issues/87))
- display distance in meters (not kilometers)
- add distance in single `/reverse/` call
- workaround python badly sniffing csv file with only one column ([#90](https://github.com/etalab/addok/issues/90))
- add housenumber in csv results ([#91](https://github.com/etalab/addok/issues/91))
- CSV: renamed "result_address" to "result_label" ([#92](https://github.com/etalab/addok/issues/92))
- no BOM by default in UTF-8
