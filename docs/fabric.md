# Déploiement avec Fabric

Vous devez obligatoirement utiliser [Fabric](http://www.fabfile.org/) avec la 
[branche v2](https://github.com/fabric/fabric/tree/v2)
pour être capable de l'exécuter avec Python 3.

## Choix d'implémentation

* toutes les commandes sont idempotents
* le fichier de configuration personnalisé doit être inspiré de `fabfile/france.fabric.yml`
  et doit être passé à chaque commande en utilisant le paramètre `--config`


## Une commande pour les gouverner toutes

```bash
fab --echo --hosts=root@ip --config=fabfile/your-config.yml bootstrap deploy reload
```

Cela va installer Addok, charger la donnée depuis `data_uri` et l'exposer 
via uwsgi/nginx.

## Configuration

### `settings`

Fichier de configuration personnalisé de Addok pour votre instance.

### `data_uri`

Lien vers un fichier JSON compressé sous forme bz2 devant être chargé.

### `domain`

Nom du domaine pour votre service.

### `plugins` (optionnel)

Liste des paquets Python devant être installés comme plugins Addok.

### `data` (optionnel)

Donnée aditionnelle devant être chargée comme une liste d'objets JSON.

### `skip_nginx` (optionnel)

Mettre à `true` si vous voulez éviter d'installer/exécuter Nginx.


## Commandes

### `system`

Commencez avec cette commande pour mettre à jour le système, installez les 
dépendances et créez l'utilisateur et les dossiers appropriés.

### `venv`

Créez l'environnement virtuel et le mettre à jour [pip](https://pip.pypa.io/en/stable/).

### `settings`

Chargez les paramètres personnalisés depuis votre fichier local référencé 
comme `settings` dans le fichier de configuration.

### `http`

Installez la configuration pour uwsgi et Nginx.

### `bootstrap` (meta)

Exécutez les commandes `system`, `venv`, `settings` et `http`.

### `fetch`

Récupérez le fichier référencé comme `data_uri` dans le fichier de configuration et le décompresser avec bzip.

### `batch`

Chargez le fichier récupéré précdemment plus de manire optionnelle la donnée venant du fichier de configuration.

### `reload` (meta)

Lancez `fetch`, arrêtez uwsgi, faire un reset de(s) base(s) de données Addok, 
lancez `batch` et redémarrez les services.

### `deploy`

Installez Addok et tous les plugins référencés comme `plugins` dans le fichier de configuration.

### `restart`

Redémarrez uwsgi et Nginx.

### `backup`

Compressez avec Bzip et télécharger la configuration, les fichiers de base de données sqlite et redis.
Le fichier téléchrgé sera nommé suivant la convention `addok-backup.YYYY-MM-DD.tar.bz2`.

### `use_backup`

Utilisez les fichiers sauvegardés antérieurement en local avec la commande `backup`
et lancez un `redis-server`.
N'oubliez pas d'utiliser le fichier de configuration approprié quand vous 
exécutez une commande addok par la suite.
