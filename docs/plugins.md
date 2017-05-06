# Plugins

## Installation d'un plugin

Chaque plugin est susceptible d'avoir son propre processus d'installation,
 mais habituellement, il faut deux étapes:

- installer un package Python, par exemple: `pip install addok-france`
- adapter votre configuration locale aux besoins du plugin

Vérifiez chaque page d'accueil d'un plugin pour avoir une documentation spécifique.


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

Note: this is only needed if you want to use hooks within your plugin.
For example, if the plugin only deals with configuration
(adding a PROCESSOR, changing the document store, etc), there is no need
for that.
Note: Il est seulement nécessaire si vous voulez utiliser un "hook" à l'intérieur
 de votre plugin. Par exemple, si le plugin ne gère que de la configuration
 (par exemple ajouter un PROCESSOR, changer le stockage de document), ce n'est pas nécessaire pour cela.

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

Si vous avez ajouté un point d'entrée à votre plugin, addok cherchera
 certains "hooks" et il les appelera si vous les avez défini.

Important: ces "hooks" doivent être dans le module défini dans le point d'entrée.


#### preconfigure(config)

Permet de modifier l'objet de configuration avant la configuration de
 l'utilisateur local (par exemple pour définir les valeurs par défaut surchargeables
 par l'utilisateur dans sa configuration locale).


#### configure(config)

Permet de modifier l'objet de configuration après la configuration de
 l'utilisateur local ait été chargée.


#### register_api_endpoint(api)

Ajoute de nouveaux points d'entrée à l'API HTTP.  Il utilise [Falcon](http://falcon.readthedocs.io/)
ainsi chaque [vue](http://falcon.readthedocs.io/en/stable/api/request_and_response.html)
doit se conformer au contrat de Falcon:

```python
class MyFalconView:

    def on_get(self, req, resp, myparameter):
        resp.body = do_something(myparameter)
        resp.status = 200
        resp.content_type = 'text/html'

def register_http_endpoint(api):
    api.add_route('/path/{myparameter}', MyFalconView())
```

#### register_http_middleware(middlewares)

Ajoute de nouveaux "middlewares" à l'API HTTP. Il utilise [Falcon](http://falcon.readthedocs.io/)
ainsi chaque [middleware](http://falcon.readthedocs.io/en/stable/api/middleware.html)
doit se conformer au contrat de Falcon:

```python
class MyFalconMiddleware:

    def process_request(self, req, resp):
        ...

    def process_resource(self, req, resp, resource, params):
        ...

    def process_response(self, req, resp, resource, req_succeeded):
        ...

def register_http_middleware(middlewares):
    middlewares.append(MyFalconMiddleware())
```

#### register_command(subparsers):

Déclare une commande pour la ligne de commande (CLI) Addok.

```python
def my_callable(*args):
    # `args` are parsed from command-line.
    do_whatever_with(args)


def register_command(subparsers):
    parser = subparsers.add_parser('mycommand', help='Documentation.')
    parser.set_defaults(func=my_callable)
```

#### register_shell_command(cmd):

Déclare une commande pour le shell Addok.  La commande doit commencer avec
 `do_` pour être reconnue en tant que commande et la commande doit être en
 majuscule.

La première ligne de de la docstring de la commande ser affichée quand `HELP`
 est utilisé dans le shell et la docstring complète sera affichée quand
 `HELP WHATEVER` est utilisé.

```python
def do_WHATEVER(cmd, remaining_string):
    """Allow to use the `WHATEVER` command within the shell."""
    # `cmd` is the Cmd instance.
    # `remaining_string` is everything typed by the user after the
    # command name.

def register_shell_command(cmd):
    cmd.register_command(do_WHATEVER)
```

## Écrire un plugin de stockage

Les plugins de stockage de documents sont des plugins particuliers étant
 donné qu'ils doivent suivre une API stricte.
A nouveau, allez-voir les plugins de stockages existants (particulièrement
 [SQLite](https://github.com/addok/addok-sqlite-store)) pour votre inspiration.

Il doit être une classe avec 4 méthodes:

### fetch(self, *keys)

Il doit faire un "yield" sur un clé et le document associé pour chacune des
 clés passées.

### upsert(self, *docs)

Doit mettre à jour ou insérer (via un update, un upsert ou un insert) les
 documents passés comme paramètres.

### remove(self, *keys)

Doit enlever les documents liés aux clés passées.

#### flushdb(self)

Doit enlever tous les documents de la base de données.
Seulement utilisé par la commande `reset`.

Une fois, que votre plugin de stockage est conforme, n'oubliez pas de mettre
 à jour le paramètre [DOCUMENT_STORE_PYPATH](config.md) pour tester le plugin.
