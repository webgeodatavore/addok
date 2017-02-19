# Installation de Addok

## Dépendances

- Redis
- python >= 3.4

## Installation en utilisant un environnement virtuel ("virtualenv")

1. Installez les dépendances:

        sudo apt-get install redis-server python3.5 python3.5-dev python-pip python-virtualenv

2. Créez un environnement virtuel:

        virtualenv addok --python=/usr/bin/python3.5

3. Activez virtualenv:

        source addok/bin/activate

4. Installez les paquets Python:

        pip install addok

## Que faire ensuite?
Maintenant, vous voulez certainement [configurer Addok](config.md), installer
des [plugins](plugins.md) ou directement [importer des données](import.md).

Voir aussi le [tutoriel d'installation](tutorial.md) complet.
