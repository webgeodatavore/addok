# Configuration de Redis

Configurer Redis peut améliorer significativement Addok.

Les conseils génériques de la documentation officielle: [ce topic](https://redis.io/topics/admin).

Voir aussi la [référence de configuration](https://redis.io/topics/config).

Sur Linux, le chemin de configuration du fichier par défault est `/etc/redis/redis.conf`.

## Persistance

Pour être capable d'arrêter et démarrer Redis sans avoir besoin d'un nouvel
 import, il est important de laisser Redis persister les données sur le disque.
Par défaut, Redis persistera chaque donnée toutes les x durées ou tous les  x
 changements dans la donnée.
La meilleure chose est de totalement désactiver la persistance automatique,
 et de le faire à la main quand c'est nécessaire. En fait, nous avons besoin de
 persister la donnée seulement après import. Quand Addok est en fonctionnement,
 il n'y a pas besoin de persister (addok créera quelques clés temporaires de
 temps à autre, mais elles sont volatiles).

Pour désactiver la sauvegarde automatique pour l'instance en fonctionnement,
 tapez:

```
redis-cli config set save ""
```

Si vous voulez la sauvegarder pour de bon, commentez les lignes `save` dans le
 fichier de configuration redis.

C'est la configuration parfaite pour exécuter Addok. Mais souvenez-vous que
 la configuration est pour l'instance Redis. Ainsi si vous avez d'autres
 services qu'Addok qui l'utilise, vous allez devoir le configurer à votre
 manière.

## Import

Quand vous importez la donnée, vous allez avoir besoin de la persister, ainsi
 un redémarrage de Redis la rechargera.

Vous pouvez soit:

- garder la configuation `save` normale de redis, qui persistera à la volée
   quand l'import s'effectue. Cela rendra l'import un peu plus lent, et
   consommera un peu plus de mémoire pendant l'import.
- lancer un `redis-cli bgsave` après l'import: c'est le scénario le plus
   rapide, parce que Redis sera prêt à être utilisé juste après l'import,
   `bgsave` étant asynchrone. Mais cela utilisera plus ou moins le double de
    mémoire quand `bgsave` exécutera, parce que Redis créera un sous-processus;
- lancer un `redis-cli save`, qui sera synchrone: cela bloquera Redis pour une
   ou deux minutes (selon la donnée que vous importez), mais il n'y aura pas
   d'usage mémoire supplémentaire


## Sécurité

Avant de passer en live/production, assurez-vous d'avoir jeté un oeil à
 [la page de sécurité](https://redis.io/topics/security).
