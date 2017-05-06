# Tutoriel

Ce tutoriel couvrira une installation à partir de zéro d'une instance Addok dédiée à la France sur un serveur Ubuntu.

Vous aurez besoin des droits sudo sur ce serveur, et il doit être connecté à Internet.

## Installer les dépendances système

    sudo apt install redis-server python3.5 python3.5-dev python-virtualenv build-essential git wget nginx uwsgi uwsgi-plugin-python3 bzip2


## Créer un utilisateur Unix

Ici, nous utilisons le nom `addok`, mais ce choix reste à votre convenance.
 Rappelez-vous de le changer au niveau des différentes commandes et fichiers
 de configuration si vous choisissez le votre.

    useradd -N addok -m -d /srv/addok/

## Créer un répertoire de configuration

    mkdir /etc/addok/
    chown addok /etc/addok

## Se connecter comme ce nouvel utilisateur

    sudo -u addok -i

A partir de maintenant, à moins que nous ne disions différemment, les commandes sont exécutées en tant qu'utilisateur `addok`.


## Créer un environnement virtuel (`virtualenv`) et l'activer

    virtualenv venv --python=/usr/bin/python3.5
    source venv/bin/activate

Note: cette activation n'est pas persistante, ainsi si vous ouvrez une
 nouvelle fenêtre de terminal, vous devrez exécutez à nouveau la
 dernière ligne.

## Installer Addok et les plugins

    pip install addok
    pip install addok-fr
    pip install addok-france

Note: si vous voulez le support du CSV par batch sur l'API HTTP, installez
 aussi le plugin `addok-csv`.

Vérifiez que l'installation a réussi jusqu'à maintenant en exécutant cette
 commande:

    addok --help

Si vous ne voyez pas d'erreur mais la liste des commandes addok, félicitations, vous pouvez continuer!

Si non, gardez courage, essayez de lire le message d'erreur, retournez aux étapes précédentes et vérifiez que tout a été fait avec succès. Et si vous êtes perdu, [créez une "issue" sur le "tracker" addok](https://github.com/addok/addok/issues) pour demander de l'aide.

## Créer un fichier de configuration local

    nano /etc/addok/addok.conf

Et collez cette configuration:
```
QUERY_PROCESSORS_PYPATHS = [
    "addok.helpers.text.check_query_length",
    "addok_france.extract_address",
    "addok_france.clean_query",
    "addok_france.remove_leading_zeros",
]
SEARCH_RESULT_PROCESSORS_PYPATHS = [
    "addok.helpers.results.match_housenumber",
    "addok_france.make_labels",
    "addok.helpers.results.score_by_importance",
    "addok.helpers.results.score_by_autocomplete_distance",
    "addok.helpers.results.score_by_ngram_distance",
    "addok.helpers.results.score_by_geo_distance",
]
PROCESSORS_PYPATHS = [
    "addok.helpers.text.tokenize",
    "addok.helpers.text.normalize",
    "addok_france.glue_ordinal",
    "addok_france.fold_ordinal",
    "addok_france.flag_housenumber",
    "addok.helpers.text.synonymize",
    "addok_fr.phonemicize",
]
```

Sauvez (ctrl+O) et fermez (Ctrl+X) le fichier.


## Télécharger la donnée BAN sous licence ODbL et la décompresser:

C'est pour la Seine-Saint-Denis, mais choisissez la zone que vous voulez
 depuis la [page de téléchargement](http://bano.openstreetmap.fr/BAN_odbl/):

    wget http://bano.openstreetmap.fr/BAN_odbl/BAN_odbl_93-json.bz2
    bunzip2 BAN_odbl_93-json.bz2

## Importer la donnée

Exécutez ces deux commandes:

    addok batch BAN_odbl_93-json
    addok ngrams

Essayons de tester que tout va bien. Exécutez le shell addok:

    addok shell

Maintenant, dans le shell Addok, tapez simplement le nom du lieu dans la zone
 que vous avez importé, et tapez "Entrée". Vous devriez voir une liste de
 résultats.
Si vous voulez une liste des commandes disponibles dans le shell, tapez "?" et
 appuyez sur "Entrée" à nouveau.

Prenez le temps de jouer avec le shell pour commencer à tester Addok.

Quand vous souhaitez continuer avec le tutoriel, tapez `QUIT` dans le shell
 Addok pour le fermer.


## Configurer l'API HTTP

Si vous voulez juste tester l'API Addok, vous pouvez simplement exécuter cette
 commande:

    addok serve

Et vous pouvez maintenant accéder à l'API via `http://127.0.0.1:7878/`.
Par exemple, pour lancer une recherche, vous devriez appeler cette URL:
[http://127.0.0.1:7878/search/?q=epinay sur seine](http://127.0.0.1:7878/search/?q=epinay sur seine
)

Mais maintenant, configurons un serveur HTTP réel.

### uWSGI

Créez un fichier nommé `/srv/addok/uwsgi_params`, avec ce contenu
 (sans faire aucun changement dessus):

```
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;

uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;

uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```

Ensuite, créez un fichier de configuration pour uWSGI:

    nano /srv/addok/uwsgi.ini

Et collez ce contenu. Vérifiez deux fois les chemins et le nom d'utilisateur
 dans le cas où vous auriez personnalisé certains d'entre eux au cours du
 tutoriel. Si vous avez suivi toutes les parties du tutoriel sans faire aucun changement, vous pouvez l'utiliser tel quel:

```
[uwsgi]
uid = addok
gid = users
# Python related settings
# the base directory (full path)
chdir           = /srv/addok/
# Addok's wsgi module
module          = addok.http.wsgi
# the virtualenv (full path)
home            = /srv/addok/venv

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 4
# the socket (use the full path to be safe
socket          = /srv/addok/uwsgi.sock
# ... with appropriate permissions - may be needed
chmod-socket    = 666
stats           = /srv/addok/stats.sock
# clear environment on exit
vacuum          = true
plugins         = python3

```

### Nginx

Créez un nouveau fichier:

    nano /srv/addok/nginx.conf

avec ce contenu:

```
# the upstream component nginx needs to connect to
upstream addok {
    server unix:///srv/addok/uwsgi.sock;
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    listen   [::]:80;
    listen      443 ssl;
    listen   [::]:443 ssl;
    # the domain name it will serve for
    server_name your-domain.org;
    charset     utf-8;

    # max upload size
    client_max_body_size 5M;   # adjust to taste

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  addok;
        include     /srv/addok/uwsgi_params;
    }
}
```

Rappelez-vous d'adapter le nom de domaine.

### Activer et redémarrer les services

Maintenant quittez la session `addok`, tapez simplement ctrl+D.

Vous devriez vous connecter en tant qu'utilisateur normal, qui est un sudoer
 (membre du groupe sudo qui permet d'exécuter `sudo`).

- Activez le fichier de configuration Nginx:

        sudo ln -s /srv/addok/nginx.conf /etc/nginx/sites-enabled/addok

- Activez le fichier de configuration uWSGI:

        sudo ln -s /srv/addok/uwsgi.ini /etc/uwsgi/apps-enabled/addok.ini

- Redémarrez les deux services:

        sudo systemctl restart uwsgi nginx


Maintenant, vous devriez être capable de lancer la recherche avec une URL comme:

    http://yourdomain.org/search/?epinay sur seine


Félicitations!

- - -

## Résolution des problèmes

- les logs Nginx sont dans /var/log/nginx/:

        sudo tail -f /var/log/nginx/error.log

  ou

        sudo tail -f /var/log/nginx/access.log

- les logs uWSGI sont dans /var/log/uwsgi:

        sudo tail -f /var/log/nginx/addok.log

- Pour vous assurer que la variable d'environnement est définie dans le shell
   actuel si vous avez changé son emplacement:

        echo $ADDOK_CONFIG_MODULE

- Exécutez `addok shell` et regardez la sortie: addok devrait retourner le fichier de configuration local, son chargement (ou sa tentative de chargement…), les plugins chargés, etc.

- Pour vérifiez la configuration de addok lui même, exécutez `addok shell` et
   tapez `CONFIG`.
  Vous serez capable de vérifier toutes les clés de configuration et vous
   assurer qu'elles ont les valeurs attendues.

- Si vos recherches ne retournent rien ou des résultats vraiment très bizarres,
 il est possible que vous ayez indexé avec une configuration différente de
 celle que vous utilisez lorsque vous faites une recherche.
