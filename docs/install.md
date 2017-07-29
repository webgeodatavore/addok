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

### Utilisez Cython (optionnel)

Pour un boost des performances, vous pouvez utiliser Cython:

```bash
pip install cython
pip install --no-binary :all: falcon
pip install --no-binary :all: addok
```

Note: cela n'est pas recommandé pour le développement.

Note: L'option `--no-binary` est seulement disponible pour les versions
 récentes de`pip`. Pour vous assurer que vous fonctionnez avec la dernière
  version, lancez `pip install -U pip`.

## Que faire ensuite?
Maintenant, vous voulez certainement [configurer Addok](config.md), installer
des [plugins](plugins.md) ou directement [importer des données](import.md).

Voir aussi le [tutoriel d'installation](tutorial.md) complet.
