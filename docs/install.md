# Installation de Addok

## Dépendances

- Redis
- python3.4

## Installation en utilisant un environnement virtuel ("virtualenv")

1. Installez les dépendances:

        sudo apt-get install redis-server python3.4 python3.4-dev python-pip python-virtualenv virtualenvwrapper

1. Créez un environnement virtuel:

        mkvirtualenv addok --python=/usr/bin/python3.4

1. installez les paquets Python:

        pip install addok

## Que faire ensuite?
Maintenant, vous voulez certainement [configurer Addok](config.md), ou directement [importer des données](import.md).
