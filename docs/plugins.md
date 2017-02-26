# Plugins

## Installation d'un plugin

Chaque plugin est susceptible d'avoir son propre processus d'installation,
 mais habituellement, il faut deux étapes:

- installer un package Python, par exemple: `pip install addok-france`
- adapter la configuration locale aux besoins du plugin

Regardez la page d'accueil d'un plugin donné pour plus de détails.


## Plugins connus

- [addok-france](https://github.com/addok/addok-france): ajout des spécificités
   des adresses France à addok (par exemple, le parsing des addresses, l'étiquetage des adresses pour le calcul du scoring, etc.)
- [addok-fr](https://github.com/addok/addok-fr): plugin dédié au support du
   Français, par exemple pour la phonémisation (meilleur tolérance de frappe).
- [addok-csv](https://github.com/addok/addok-csv): ajout d'un point d'entrée
   CSV pour votre serveur Addok (pour le géocodage par batch de fichiers CSV)
- [addok-psql](https://github.com/addok/addok-psql): import depuis une base de
   données PosgreSQL dans Addok.
- [addok-trigrams](https://github.com/addok/addok-trigrams): algorithme d'indexation alternatif basé sur les trigrammes.
- [addok-sqlite-store](https://github.com/addok/addok-sqlite-store): stockage des doucments dans SQLite.

## Écrire un plugin

Comme d'habitude, la meilleure manière d'apprendre est regarder dans le code:
 jetez un oeil aux autres plugins pour une inspiration.

### Anatomie d'un plugin

Un plugin Addok est simplement un module Python:

- il doit être installé dans le PYTHONPATH pour qu'addok soit capable de
   l'importer
- il doit avoir le point d'entrée `addok.ext` dans le cas où il nécessite
   d'utiliser les endpoints de l'API

### point d'entrée addok.ext

Note: Il est seulement nécessaire si vous voulez votre plugin connecté aux
 endpoints de l'API. Si le plugin doit seulement gérer de la configuration
 (par exemple ajouter un PROCESSOR), ce n'est pas nécessaire pour cela.

Ajouter ceci à votre `setup.py`:

```python
setup(
    name='addok-mysuperplugin',
    …,
    entry_points={'addok.ext': ['mysuperplugin=relative.path.to.plugin']},
)
```

Disons par exemple que la structure du plugin est:

```
mysuperplugin/
    setup.py
    README.md
    mysuperplugin/
        __init__.py
        utils.py
        hooks.py
```

Si vous devez mettre les "hooks" dans `hooks.py`, alors votre point d'entrée devrait être:

```python
    entry_points={'addok.ext': ['mysuperplugin=mysuperplugin.hooks']},
```

### API des plugins

Si vous avez ajouté un point d'entrée à votre plugin, addok cherchera certains "hooks" et il les appelera si vous les avez défini.

Important: ces "hooks" doivent être dans le module défini dans le point d'entrée.


#### preconfigure(config)

Permet de configurer le chemin de configuration de l'objet avant la configuration de l'utilisateur local (par exemple pour définir les valeurs par défaut surchargeables alors par l'utilisateur du plugin dans sa configuration locale).


#### configure(config)

Permet de configurer le chemin de configuration de l'objet après la configuration de l'utilisateur local.


#### register_api_endpoint(api)

Ajoute de nouveaux points d'entrée à l'API HTTP.


#### register_api_middleware(middlewares)

Ajoute de nouveaux "middlewares" à l'API HTTP.


#### register_command(subparsers):

Déclare une commande pour la ligne de commande (CLI) Addok.


#### register_shell_command(cmd):

Déclare une commande pour le shell Addok.


## Écrire un plugin de stockage

Les plugins de stockage de documents sont des plugins particuliers étant donné qu'ils doivent suivre une API stricte.
A nouveau, allez-voir les plugins de stockages existants (particulièrement [SQLite](https://github.com/addok/addok-sqlite-store)) pour votre inspiration.

Il doit être une classe avec 4 méthodes:

### fetch(self, *keys)

Il doit faire un "yield" sur un clé et le document associé pour chacune des clés passées.

### upsert(self, *docs)

Doit mettre à jour ou insérer (via un update, un upsert ou un insert) les documents passés comme paramètres.

### remove(self, *keys)

Doit enlever les documents lis aux clés passées.

#### flushdb(self)

Doit enlever tous les documents de la base de données.
Seulement utilisé par la commande `reset`.

Une fois, que votre plugin de stockage est conforme, n'oubliez pas de mettre à jour le paramètre [DOCUMENT_STORE_PYPATH](config.md) pour tester le plugin.
