# Bienvenue à la documentation de Addok

*Un moteur de recherche pour les adresses. Rien que les adresses.*

## Aperçu

Addok fonctionne avec Redis en back-end.

- il importe et indexe vos données (et peut aussi être importé depuis une base de données Nominatim) en ligne de commande
- il sert une API minimale basée sur du GeoJSON (avec Falcon)
- il fait du géocodage inversé ("reverse geocoding")
- il fait du géocodage par batch (via du CSV pour le moment)
- il fournit une ligne de commande de debug pour inspecter l'index
- il est extensible par des plugins
- il est open source

Commencez par [l'installer](install.md) et comprendre les [concepts](concepts.md) sous-jacents.

## Montrez-nous le code

Le code est publié via [Github](https://github.com/etalab/addok/).

## Licence

Addok est mis à disposition sous licence WTFPL.
